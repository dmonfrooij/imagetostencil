import { useState } from 'react'
import ImageUpload from './components/ImageUpload'
import Preview from './components/Preview'
import Controls from './components/Controls'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [previewData, setPreviewData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [settings, setSettings] = useState({
    threshold: 128,
    extrusion_height: 5.0,
    wall_thickness: 2.0,
    format: 'stl'
  })

  const handleFileUpload = (uploadedFile) => {
    setFile(uploadedFile)
    setError(null)
  }

  const handlePreview = async () => {
    if (!file) {
      setError('Please upload an image first')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('threshold', settings.threshold)
      formData.append('extrusion_height', settings.extrusion_height)
      formData.append('wall_thickness', settings.wall_thickness)

      const response = await fetch('/api/preview', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to generate preview')
      }

      const data = await response.json()
      setPreviewData(data)
    } catch (err) {
      setError(err.message)
      console.error('Preview error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = async () => {
    if (!file) {
      setError('Please upload an image first')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('threshold', settings.threshold)
      formData.append('extrusion_height', settings.extrusion_height)
      formData.append('wall_thickness', settings.wall_thickness)
      formData.append('format', settings.format)

      const response = await fetch('/api/generate', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to generate stencil')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `stencil.${settings.format}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      setError(err.message)
      console.error('Download error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSettingsChange = (newSettings) => {
    setSettings(newSettings)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">🎨 Image to Stencil</h1>
          <p className="text-gray-600">Convert your images into 3D printable stencils for spray painting</p>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            <strong>Error:</strong> {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left panel - Upload and Controls */}
          <div className="lg:col-span-1 space-y-6">
            <ImageUpload onFileUpload={handleFileUpload} file={file} />
            <Controls 
              settings={settings} 
              onSettingsChange={handleSettingsChange}
            />
            <div className="space-y-2">
              <button
                onClick={handlePreview}
                disabled={!file || loading}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
              >
                {loading ? 'Processing...' : '👁️ Preview'}
              </button>
              <button
                onClick={handleDownload}
                disabled={!file || loading}
                className="w-full px-4 py-2 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
              >
                {loading ? 'Processing...' : '📥 Download'}
              </button>
            </div>
          </div>

          {/* Right panel - Preview */}
          <div className="lg:col-span-2">
            <Preview previewData={previewData} loading={loading} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
