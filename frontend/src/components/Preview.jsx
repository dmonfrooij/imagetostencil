import { useEffect, useRef } from 'react'
import * as THREE from 'three'

function Preview({ previewData, loading }) {
  const containerRef = useRef(null)
  const sceneRef = useRef(null)
  const cameraRef = useRef(null)
  const rendererRef = useRef(null)
  const meshRef = useRef(null)

  useEffect(() => {
    if (!containerRef.current) return

    // Initialize scene
    if (!sceneRef.current) {
      const scene = new THREE.Scene()
      scene.background = new THREE.Color(0xf5f5f5)

      const camera = new THREE.PerspectiveCamera(
        75,
        containerRef.current.clientWidth / containerRef.current.clientHeight,
        0.1,
        1000
      )
      camera.position.z = 50

      const renderer = new THREE.WebGLRenderer({ antialias: true })
      renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight)
      renderer.shadowMap.enabled = true
      containerRef.current.appendChild(renderer.domElement)

      // Lights
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
      scene.add(ambientLight)

      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6)
      directionalLight.position.set(10, 10, 10)
      directionalLight.castShadow = true
      scene.add(directionalLight)

      sceneRef.current = scene
      cameraRef.current = camera
      rendererRef.current = renderer

      // Animation loop
      const animate = () => {
        requestAnimationFrame(animate)
        if (meshRef.current) {
          meshRef.current.rotation.x += 0.003
          meshRef.current.rotation.y += 0.005
        }
        renderer.render(scene, camera)
      }
      animate()

      // Handle window resize
      const handleResize = () => {
        if (!containerRef.current) return
        const width = containerRef.current.clientWidth
        const height = containerRef.current.clientHeight
        camera.aspect = width / height
        camera.updateProjectionMatrix()
        renderer.setSize(width, height)
      }
      window.addEventListener('resize', handleResize)

      return () => window.removeEventListener('resize', handleResize)
    }
  }, [])

  useEffect(() => {
    if (!previewData || !sceneRef.current) return

    // Remove previous mesh
    if (meshRef.current) {
      sceneRef.current.remove(meshRef.current)
    }

    try {
      const geometry = new THREE.BufferGeometry()
      geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(previewData.vertices.flat()), 3))
      geometry.setIndex(new THREE.BufferAttribute(new Uint32Array(previewData.faces.flat()), 1))
      geometry.computeVertexNormals()

      const material = new THREE.MeshStandardMaterial({
        color: 0x667eea,
        metalness: 0.4,
        roughness: 0.6,
        side: THREE.DoubleSide
      })

      const mesh = new THREE.Mesh(geometry, material)
      sceneRef.current.add(mesh)
      meshRef.current = mesh

      // Auto-scale and center
      geometry.center()
      const box = new THREE.Box3().setFromObject(mesh)
      const size = box.getSize(new THREE.Vector3())
      const maxDim = Math.max(size.x, size.y, size.z)
      const scale = 40 / maxDim
      mesh.scale.multiplyScalar(scale)
    } catch (error) {
      console.error('Error creating preview:', error)
    }
  }, [previewData])

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden h-full min-h-96 flex flex-col">
      <div className="bg-gray-100 px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-bold text-gray-800">🔍 3D Preview</h2>
      </div>
      <div className="flex-1 relative bg-gradient-to-b from-gray-50 to-gray-100">
        <div
          ref={containerRef}
          className="w-full h-full"
        />
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 rounded">
            <div className="text-white text-center">
              <div className="mb-2">⏳ Generating preview...</div>
              <div className="text-sm">This may take a moment</div>
            </div>
          </div>
        )}
        {!previewData && !loading && (
          <div className="absolute inset-0 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <div className="text-4xl mb-2">🎬</div>
              <p>Upload an image and click Preview to see it here</p>
            </div>
          </div>
        )}
        {previewData && (
          <div className="absolute bottom-4 right-4 bg-black bg-opacity-70 text-white px-3 py-2 rounded text-sm">
            <div>📊 Stats:</div>
            <div className="text-xs">Vertices: {previewData.stats.vertex_count}</div>
            <div className="text-xs">Faces: {previewData.stats.face_count}</div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Preview
