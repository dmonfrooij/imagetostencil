# Image to Stencil Generator

Free 3D STL/3MF stencil generator from images. Convert your photos into printable 3D stencils for spray painting!

## Features

✨ **Image to 3D Conversion**
- Upload JPG, PNG images
- Automatic edge detection and vectorization
- Customizable threshold and parameters
- Real-time preview

🎨 **Stencil Generation**
- Generate STL and 3MF files
- Adjustable extrusion height
- Wall thickness control
- Drainage holes support

🖨️ **3D Print Ready**
- Download in STL format (universal 3D printer format)
- Download in 3MF format (modern 3D format)
- Optimized for FDM printing

## Tech Stack

**Frontend:**
- React.js
- Three.js (3D preview)
- Tailwind CSS

**Backend:**
- Python Flask/FastAPI
- OpenCV (image processing)
- Trimesh (3D mesh generation)
- NumPy, Pillow

## Project Structure

```
imagetostencil/
├── frontend/                 # React web interface
│   ├── public/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── backend/                  # Python API server
│   ├── app.py               # Flask app
│   ├── image_processor.py   # Image processing logic
│   ├── stencil_generator.py # 3D generation
│   ├── requirements.txt
│   └── uploads/            # Temporary file storage
└── README.md
```

## Quick Start

### Prerequisites
- Node.js 16+
- Python 3.8+

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## Usage

1. Open http://localhost:5173 in your browser
2. Upload an image (JPG, PNG)
3. Adjust settings:
   - Threshold (edge detection sensitivity)
   - Extrusion height
   - Wall thickness
4. Preview the 3D model
5. Download as STL or 3MF

## API Endpoints

`POST /api/generate` - Generate stencil from image
- Request: multipart/form-data with image file
- Response: STL file

`GET /api/preview` - Get 3D model preview data

## Configuration

Edit `backend/config.py`:
- `MAX_IMAGE_SIZE` - Maximum upload size
- `DEFAULT_EXTRUSION_HEIGHT` - Default 3D height
- `DEFAULT_WALL_THICKNESS` - Default wall thickness

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - See LICENSE file for details

## Roadmap

- [ ] Batch processing
- [ ] Advanced filters (blur, sharpen)
- [ ] Custom stencil templates
- [ ] Real-time collaboration
- [ ] Community stencil gallery

---

Made with ❤️ for makers and artists
