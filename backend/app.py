from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
from image_processor import ImageProcessor
from stencil_generator import StencilGenerator
import logging

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

@app.route('/api/generate', methods=['POST'])
def generate_stencil():
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, bmp'}), 400
        
        # Get parameters
        threshold = int(request.form.get('threshold', 128))
        extrusion_height = float(request.form.get('extrusion_height', 5.0))
        wall_thickness = float(request.form.get('wall_thickness', 2.0))
        format_type = request.form.get('format', 'stl').lower()
        
        # Validate parameters
        threshold = max(1, min(255, threshold))
        extrusion_height = max(0.5, min(50.0, extrusion_height))
        wall_thickness = max(0.5, min(10.0, wall_thickness))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        filepath = os.path.join(UPLOAD_FOLDER, f"{file_id}_{filename}")
        file.save(filepath)
        
        # Process image
        processor = ImageProcessor(filepath)
        processed_image = processor.process(
            threshold=threshold,
            apply_canny=True
        )
        
        # Generate stencil
        generator = StencilGenerator(processed_image)
        mesh = generator.generate_mesh(
            extrusion_height=extrusion_height,
            wall_thickness=wall_thickness
        )
        
        # Save output
        output_id = str(uuid.uuid4())
        if format_type == '3mf':
            output_path = os.path.join(UPLOAD_FOLDER, f"{output_id}_stencil.3mf")
        else:
            output_path = os.path.join(UPLOAD_FOLDER, f"{output_id}_stencil.stl")
        
        mesh.export(output_path)
        
        # Clean up input file
        os.remove(filepath)
        
        # Send file
        return send_file(
            output_path,
            as_attachment=True,
            download_name=f"stencil.{format_type}"
        )
    
    except Exception as e:
        logger.error(f"Error generating stencil: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/preview', methods=['POST'])
def preview_stencil():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Get parameters
        threshold = int(request.form.get('threshold', 128))
        extrusion_height = float(request.form.get('extrusion_height', 5.0))
        wall_thickness = float(request.form.get('wall_thickness', 2.0))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        filepath = os.path.join(UPLOAD_FOLDER, f"{file_id}_{filename}")
        file.save(filepath)
        
        # Process image
        processor = ImageProcessor(filepath)
        processed_image = processor.process(threshold=threshold)
        
        # Generate stencil
        generator = StencilGenerator(processed_image)
        mesh = generator.generate_mesh(
            extrusion_height=extrusion_height,
            wall_thickness=wall_thickness
        )
        
        # Get mesh data for preview
        vertices = mesh.vertices.tolist()
        faces = mesh.faces.tolist()
        bounds = {
            'min': mesh.bounds[0].tolist(),
            'max': mesh.bounds[1].tolist()
        }
        
        # Clean up
        os.remove(filepath)
        
        return jsonify({
            'vertices': vertices,
            'faces': faces,
            'bounds': bounds,
            'stats': {
                'vertex_count': len(vertices),
                'face_count': len(faces)
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Error creating preview: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
