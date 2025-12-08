# Camera Streaming Toolkit

A lightweight collection of OpenCV utilities plus a Flask web server for experimenting with live camera feeds, face detection, and bright-spot tracking. The project targets Raspberry Pi or PC webcams but runs anywhere Python and OpenCV are available.

## Features
- **Flask video streamer (`raspi.py`)** – captures frames from a webcam, highlights the brightest blob with an ellipse/crosshair, and serves the annotated stream over MJPEG.
- **Bright-spot desktop tester (`cvtest.py`)** – quickly previews the contour-based highlight logic without running Flask.
- **Face-detection demo (`pc_get.py`)** – uses an LBP cascade to detect the largest face in view and draw a bounding box.
- **Simple frontend (`templates/index.html`)** – renders the MJPEG feed in any browser on the same network.

## Requirements
- Python 3.9+ (tested with CPython)
- OpenCV (`opencv-python`)
- Flask
- NumPy

Install dependencies into your environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install flask opencv-python numpy
```

## Usage
### 1. Face-detection test on a PC
```powershell
python pc_get.py
```
- Update `FaceCascade` in `pc_get.py` if your cascade file lives elsewhere (the repo ships `lbpcascade_frontalface_improved.xml`).
- Press `Esc` to close the preview window.

### 2. Bright-spot experiment without Flask
```powershell
python cvtest.py
```
- Adjust the binary threshold (`cv2.threshold(..., 230, ...)`) if your lighting differs.

### 3. Serve processed video over Flask
```powershell
python raspi.py
```
1. Edit `cap = cv2.VideoCapture(0)` if your camera enumerates under a different index.
2. Set `app.run(host=..., port=...)` to the IP/port reachable by your clients (e.g., your Raspberry Pi LAN address).
3. Visit `http://<host>:<port>/` from a browser to see the stream.

## Project Layout
```
├── cvtest.py                   # Local bright-spot visualization
├── lbpcascade_frontalface_improved.xml
├── pc_get.py                   # Face detection demo
├── raspi.py                    # Flask MJPEG streamer
├── templates/
│   └── index.html              # Simple MJPEG consumer page
└── LICENSE
```

## Customization Tips
- Lower the `cv2.threshold` value in `raspi.py`/`cvtest.py` for dimmer scenes, or increase it to ignore noise.
- Swap in a different Haar/LBP cascade in `pc_get.py` to detect other objects; be sure to update the path.
- For higher latency tolerance but better quality, tweak the JPEG encoding call (`cv2.imencode`) with different quality parameters.

## Troubleshooting
- **No camera detected**: confirm another app is not using the device, or change the `VideoCapture` index.
- **Blank stream in browser**: make sure the client can reach the host/port and that firewall rules allow inbound HTTP.
- **Slow frame rate**: disable debug builds of OpenCV, lower the camera resolution, or resize frames before encoding.

## License
Distributed under the terms described in `LICENSE`.
