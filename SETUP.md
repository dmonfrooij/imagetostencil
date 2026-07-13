# Image to Stencil Generator - Installation & Setup Guide

## Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **Git**

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/dmonfrooij/imagetostencil.git
cd imagetostencil
```

### 2. Backend Setup

#### Option A: Using Python venv (Recommended)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
python app.py
```

Backend will be available at: `http://localhost:5000`

#### Option B: Using Docker

```bash
cd backend
docker build -t imagetostencil-backend .
docker run -p 5000:5000 imagetostencil-backend
```

### 3. Frontend Setup

In a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## Usage

1. Open your browser to `http://localhost:5173`
2. Upload an image (JPG, PNG, GIF, or BMP)
3. Adjust the settings:
   - **Threshold**: Controls edge detection sensitivity (1-255)
   - **Extrusion Height**: Height of the 3D stencil (0.5-50mm)
   - **Wall Thickness**: Thickness of stencil walls (0.5-10mm)
   - **Format**: Choose STL or 3MF export format
4. Click **Preview** to see the 3D model
5. Click **Download** to save your stencil file

## API Endpoints

### Generate Stencil

```
POST /api/generate
```

**Parameters (multipart/form-data):**
- `file` (required): Image file (PNG, JPG, GIF, BMP)
- `threshold` (optional, default: 128): Edge detection threshold (1-255)
- `extrusion_height` (optional, default: 5.0): Height in mm (0.5-50)
- `wall_thickness` (optional, default: 2.0): Wall thickness in mm (0.5-10)
- `format` (optional, default: stl): Export format (stl or 3mf)

**Response:** Binary STL or 3MF file

### Generate Preview

```
POST /api/preview
```

**Parameters (multipart/form-data):**
- `file` (required): Image file
- `threshold` (optional): Edge detection threshold
- `extrusion_height` (optional): Height in mm
- `wall_thickness` (optional): Wall thickness in mm

**Response (JSON):**
```json
{
  "vertices": [[x, y, z], ...],
  "faces": [[i, j, k], ...],
  "bounds": {
    "min": [x, y, z],
    "max": [x, y, z]
  },
  "stats": {
    "vertex_count": 1000,
    "face_count": 800
  }
}
```

## Configuration

### Backend Configuration

Edit `backend/config.py`:

```python
DEFAULT_EXTRUSION_HEIGHT = 5.0      # mm
DEFAULT_WALL_THICKNESS = 2.0        # mm
DEFAULT_THRESHOLD = 128              # 0-255
DEFAULT_SCALE = 0.1                 # pixels to mm conversion
```

### Frontend Configuration

Edit `frontend/vite.config.js` to change the backend proxy URL:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:5000',  // Change this
    changeOrigin: true,
  }
}
```

## Building for Production

### Frontend

```bash
cd frontend
npm run build
```

Output will be in `frontend/dist/`

### Backend

```bash
cd backend
# Using Gunicorn (production WSGI server)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### Backend won't start
- Make sure Python 3.8+ is installed: `python --version`
- Check if port 5000 is in use: `lsof -i :5000` (macOS/Linux)
- Try clearing pip cache: `pip cache purge`

### Frontend won't load
- Check Node.js version: `node --version` (should be 16+)
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

### Preview not loading
- Check browser console for errors (F12)
- Ensure backend is running on port 5000
- Try a smaller image file

### 3D model looks wrong
- Adjust the **Threshold** value (try lower values for more detail)
- Try **Extrusion Height** adjustment
- Ensure your image has good contrast between foreground and background

## Dependencies

### Backend
- Flask - Web framework
- OpenCV - Image processing
- Trimesh - 3D mesh generation
- NumPy, Pillow - Image manipulation

### Frontend
- React - UI framework
- Three.js - 3D visualization
- Tailwind CSS - Styling
- Vite - Build tool

## Development

### Running tests (Backend)

```bash
cd backend
python -m pytest tests/
```

### Code formatting (Backend)

```bash
cd backend
black .
pylint *.py
```

### Linting (Frontend)

```bash
cd frontend
npm run lint
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please create a GitHub issue.

## Roadmap

- [ ] Batch processing support
- [ ] Advanced image filters (blur, sharpen, contrast)
- [ ] Custom stencil templates
- [ ] Real-time collaboration
- [ ] Community stencil gallery
- [ ] Mobile app
- [ ] WebAssembly optimization

---

Happy stenciling! 🎨
