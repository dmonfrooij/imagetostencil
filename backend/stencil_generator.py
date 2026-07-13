import numpy as np
import cv2
import trimesh
from scipy import ndimage
import logging

logger = logging.getLogger(__name__)

class StencilGenerator:
    """Generate 3D stencils from processed images"""
    
    def __init__(self, processed_image):
        """
        Initialize with processed (binary) image
        
        Args:
            processed_image: Binary image (255 for stencil, 0 for background)
        """
        self.image = processed_image
        self.height, self.width = processed_image.shape
        logger.info(f"StencilGenerator initialized with image size: {self.width}x{self.height}")
    
    def get_contours(self, min_area=10):
        """Extract contours from image"""
        contours, _ = cv2.findContours(self.image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter by minimum area
        filtered_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= min_area:
                filtered_contours.append(contour)
        
        logger.info(f"Found {len(filtered_contours)} contours")
        return filtered_contours
    
    def contour_to_3d_points(self, contour, extrusion_height=5.0, scale=0.1):
        """
        Convert 2D contour to 3D points
        
        Args:
            contour: OpenCV contour
            extrusion_height: Height of extrusion in mm
            scale: Scale factor for XY coordinates
        """
        # Get contour points
        points_2d = contour.reshape(-1, 2).astype(np.float32)
        
        # Scale points
        points_2d = points_2d * scale
        
        # Center the points
        center = np.mean(points_2d, axis=0)
        points_2d = points_2d - center
        
        # Create 3D points (bottom and top)
        points_bottom = np.column_stack([points_2d, np.zeros(len(points_2d))])
        points_top = np.column_stack([points_2d, np.full(len(points_2d), extrusion_height)])
        
        return points_bottom, points_top
    
    def create_extrusion_mesh(self, points_2d, extrusion_height=5.0, wall_thickness=2.0):
        """
        Create a hollow extrusion (walls) from 2D points
        
        Args:
            points_2d: 2D points (N, 2)
            extrusion_height: Height of extrusion
            wall_thickness: Thickness of the walls
        """
        n_points = len(points_2d)
        
        # Outer contour (original)
        outer_2d = points_2d.copy()
        
        # Inner contour (offset inward)
        center = np.mean(outer_2d, axis=0)
        direction = outer_2d - center
        norm = np.linalg.norm(direction, axis=1, keepdims=True)
        norm[norm == 0] = 1  # Avoid division by zero
        direction = direction / norm
        
        inner_2d = outer_2d - direction * wall_thickness
        
        # Create 3D vertices
        # Bottom layer
        outer_bottom = np.column_stack([outer_2d, np.zeros(n_points)])
        inner_bottom = np.column_stack([inner_2d, np.zeros(n_points)])
        
        # Top layer
        outer_top = np.column_stack([outer_2d, np.full(n_points, extrusion_height)])
        inner_top = np.column_stack([inner_2d, np.full(n_points, extrusion_height)])
        
        vertices = np.vstack([outer_bottom, inner_bottom, outer_top, inner_top])
        
        # Create faces (walls)
        faces = []
        
        # Outer walls
        for i in range(n_points):
            next_i = (i + 1) % n_points
            # Bottom face
            faces.append([i, next_i, n_points + next_i])
            faces.append([i, n_points + next_i, n_points + i])
            # Top face
            faces.append([2*n_points + i, 2*n_points + next_i, 3*n_points + next_i])
            faces.append([2*n_points + i, 3*n_points + next_i, 3*n_points + i])
            # Side walls
            faces.append([i, next_i, 2*n_points + next_i])
            faces.append([i, 2*n_points + next_i, 2*n_points + i])
        
        # Inner walls
        for i in range(n_points):
            next_i = (i + 1) % n_points
            faces.append([n_points + next_i, n_points + i, 3*n_points + i])
            faces.append([n_points + next_i, 3*n_points + i, 3*n_points + next_i])
        
        faces = np.array(faces)
        
        return trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    
    def generate_mesh(self, extrusion_height=5.0, wall_thickness=2.0, scale=0.1):
        """
        Generate 3D mesh from processed image
        
        Args:
            extrusion_height: Height to extrude in mm
            wall_thickness: Thickness of the walls in mm
            scale: Scale factor for converting pixels to mm
        
        Returns:
            trimesh.Trimesh: Generated 3D mesh
        """
        logger.info(f"Generating mesh with extrusion_height={extrusion_height}, wall_thickness={wall_thickness}")
        
        contours = self.get_contours(min_area=20)
        
        if not contours:
            logger.warning("No contours found. Creating default mesh.")
            # Create a simple box
            return trimesh.creation.box(width=10, height=10, height=extrusion_height)
        
        meshes = []
        
        for contour in contours:
            # Simplify contour
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            
            if len(approx) < 3:
                continue
            
            # Convert to 2D points
            points_2d = approx.reshape(-1, 2).astype(np.float32)
            
            # Check if contour is valid (not self-intersecting)
            try:
                mesh = self.create_extrusion_mesh(
                    points_2d,
                    extrusion_height=extrusion_height,
                    wall_thickness=wall_thickness
                )
                if mesh.is_valid:
                    meshes.append(mesh)
                else:
                    logger.warning("Invalid mesh created, skipping contour")
            except Exception as e:
                logger.warning(f"Failed to create mesh for contour: {str(e)}")
                continue
        
        if not meshes:
            logger.warning("No valid meshes created. Creating default mesh.")
            return trimesh.creation.box(width=10, height=10, height=extrusion_height)
        
        # Combine all meshes
        combined_mesh = trimesh.util.concatenate(meshes)
        
        # Clean up the mesh
        combined_mesh.remove_degenerate_faces()
        combined_mesh.remove_infinite_values()
        
        logger.info(f"Generated mesh with {len(combined_mesh.vertices)} vertices and {len(combined_mesh.faces)} faces")
        
        return combined_mesh
