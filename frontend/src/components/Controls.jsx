import { useState } from 'react'

function Controls({ settings, onSettingsChange }) {
  const handleChange = (key, value) => {
    const newSettings = { ...settings, [key]: value }
    onSettingsChange(newSettings)
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">⚙️ Settings</h2>

      <div className="space-y-4">
        {/* Threshold */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Threshold: {settings.threshold}
          </label>
          <input
            type="range"
            min="1"
            max="255"
            value={settings.threshold}
            onChange={(e) => handleChange('threshold', parseInt(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
          <p className="text-xs text-gray-500 mt-1">Lower = more detail, Higher = simpler shape</p>
        </div>

        {/* Extrusion Height */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Extrusion Height: {settings.extrusion_height.toFixed(1)}mm
          </label>
          <input
            type="range"
            min="0.5"
            max="50"
            step="0.5"
            value={settings.extrusion_height}
            onChange={(e) => handleChange('extrusion_height', parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
          <p className="text-xs text-gray-500 mt-1">Height of the 3D stencil</p>
        </div>

        {/* Wall Thickness */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Wall Thickness: {settings.wall_thickness.toFixed(1)}mm
          </label>
          <input
            type="range"
            min="0.5"
            max="10"
            step="0.5"
            value={settings.wall_thickness}
            onChange={(e) => handleChange('wall_thickness', parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
          <p className="text-xs text-gray-500 mt-1">Thickness of the stencil walls</p>
        </div>

        {/* Format Selection */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">📦 Export Format</label>
          <select
            value={settings.format}
            onChange={(e) => handleChange('format', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="stl">STL (Standard)</option>
            <option value="3mf">3MF (Modern)</option>
          </select>
          <p className="text-xs text-gray-500 mt-1">STL is more widely supported</p>
        </div>
      </div>
    </div>
  )
}

export default Controls
