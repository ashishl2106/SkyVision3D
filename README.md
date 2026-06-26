# SkyVision3D

A professional 3D planetarium and live flight tracking application with real-time video capture capabilities. Designed for museum-quality interactive displays, large LED walls, and ceiling projections.

## Features

### Core Features
- **Photorealistic Earth**: 8K texture with cloud layer, atmosphere, and night lights
- **Live Flight Tracking**: Real-time aircraft position data from multiple providers
- **Live Video Capture**: Integrate live video feeds from cameras
- **Solar System**: Accurate planetary positions using NASA ephemeris data
- **60 FPS Performance**: Optimized for 4K resolution (3840x2160)
- **Professional UI**: FPS counter, time display, search, settings
- **Museum Mode**: Automatic camera animations, touchscreen support

### Technical Highlights
- Modern OpenGL with advanced shaders
- HDR rendering with bloom post-processing
- Instanced rendering for thousands of aircraft
- Smooth interpolation and LOD systems
- Rotating logs and performance monitoring
- Comprehensive type hints and documentation

## Requirements

- Python 3.12 or higher
- OpenGL 4.3 or higher capable GPU
- 4GB RAM minimum (8GB recommended)
- 2GB disk space for assets

## Installation

### From Source

```bash
git clone https://github.com/ashishl2106/SkyVision3D.git
cd SkyVision3D
pip install -r requirements.txt
```

### Running the Application

```bash
python -m app.main
```

### Running Tests

```bash
pip install -r requirements.txt[dev]
pytest tests/
pytest tests/ --cov=app
```

## Project Structure

```
SkyVision3D/
├── app/                      # Main application package
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── core/                # Core engine components
│   ├── renderer/            # OpenGL rendering engine
│   ├── earth/               # Earth rendering system
│   ├── flights/             # Flight tracking system
│   ├── planets/             # Solar system rendering
│   ├── ui/                  # User interface components
│   ├── capture/             # Video capture system
│   └── utils/               # Utility modules
├── assets/                  # Game assets
│   ├── shaders/             # GLSL shader files
│   ├── textures/            # Texture files
│   ├── models/              # 3D model files
│   └── fonts/               # Font files
├── tests/                   # Unit and integration tests
├── docs/                    # Documentation
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
├── settings.json           # Application settings
└── README.md              # This file
```

## Configuration

Edit `settings.json` to customize:
- Resolution (default: 3840x2160)
- Target FPS (default: 60)
- Texture quality (low/medium/high)
- Flight refresh rate
- Planet update rate
- Language support

## Usage

### Mouse Controls
- **Left Click + Drag**: Orbit camera
- **Right Click + Drag**: Pan camera
- **Scroll Wheel**: Zoom in/out

### Keyboard Controls
- **F**: Toggle fullscreen
- **P**: Toggle projection mode
- **M**: Toggle museum mode
- **S**: Settings menu
- **ESC**: Quit

### Touchscreen (Museum Mode)
- Pinch to zoom
- Swipe to pan
- Long-press for information

## Flight Data Providers

### OpenSky Network
- Real-time ADS-B data
- Free public API
- ~10,000-30,000 aircraft globally

### ADS-B Exchange
- Enhanced ADS-B coverage
- Higher update frequency
- Extended aircraft information

### Replay Mode
- Pre-recorded flight data
- Useful for demonstrations

## Video Capture

- Support for webcams and IP cameras
- Real-time overlay on 3D scene
- Multiple capture profiles
- Hardware acceleration where available

## Performance

- **Target**: 60 FPS at 4K resolution
- **CPU**: Multi-threaded flight and planet updates
- **GPU**: Instanced rendering, texture atlasing
- **Memory**: Optimized asset loading

## Building Executable

```bash
pip install PyInstaller
pyinstaller --onefile --windowed app/main.py
```

Executable will be in `dist/` directory.

## Documentation

See `docs/` directory for:
- Architecture overview
- Shader documentation
- API reference
- Development guide

## License

MIT License - See LICENSE file for details

## Credits

- **Skyfield**: Astronomical calculations
- **ModernGL**: OpenGL bindings
- **OpenSky Network**: Flight data provider
- **NASA JPL**: Ephemeris data

## Support

For issues, feature requests, or questions:
- GitHub Issues: https://github.com/ashishl2106/SkyVision3D/issues
- Documentation: https://github.com/ashishl2106/SkyVision3D/wiki
