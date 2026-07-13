# Contributing to Image to Stencil

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/imagetostencil.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Commit with clear messages: `git commit -m 'Add: description'`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Open a Pull Request

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints where possible
- Max line length: 120 characters
- Use meaningful variable names

```python
def process_image(image_path: str, threshold: int = 128) -> np.ndarray:
    """Process image with given threshold."""
    pass
```

### JavaScript (Frontend)
- Use ES6+ features
- Use functional components (React Hooks)
- Props validation with PropTypes or TypeScript
- Max line length: 100 characters

```javascript
function MyComponent({ prop1, prop2 = 'default' }) {
  return <div>{prop1}</div>
}
```

## Commit Message Format

```
<type>: <subject>

<body>
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style (no logic changes)
- `refactor:` Code refactoring
- `perf:` Performance improvement
- `test:` Adding tests

**Example:**
```
feat: Add support for GIF images

Implement GIF frame selection for stencil generation.
- Extract first frame from GIF
- Add UI control for frame selection
- Update image processor
```

## Testing

Before submitting a PR:

### Backend
```bash
cd backend
pip install pytest pytest-cov
pytest tests/ -v --cov=.
```

### Frontend
```bash
cd frontend
npm run lint
```

## Pull Request Process

1. Update README.md with any new features
2. Add tests for new functionality
3. Ensure all tests pass
4. Fill out the PR template
5. Link any related issues

## Report Bugs

Create a GitHub issue with:
- Clear title
- Detailed description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- System info (OS, Python/Node version)

## Suggest Features

Create a GitHub issue with:
- Clear title starting with `Feature:`
- Detailed description of the feature
- Why it would be useful
- Possible implementation approach

## Questions?

Feel free to open a GitHub discussion or issue.
