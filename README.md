# NVR Viewer

My NVR system uses Flash for web display. Now that Flash is disabled, I needed a way to casually view my cameras from my desktop.

This is a simple script which uses TKinter and PIL to grab each channel's image snapshot and display it (stacked).

The snapshots resize to the window's size and overlays the current time.

Each snapshot will update every two seconds.

## Installation

Requires Python 3.6 or higher, PIL, and TKinter

1. `source .env/bin/activate && pyton3 -m pip install -r requirements.txt`
2. Copy/rename `nvr-viewer.desktop.dist` to `nvr-viewer.desktop`.
3. Fill in the environment variables for username, password, IP, and channels in `nvr-viewer.desktop`.
4. Move or symlink the desktop file `~/.local/share/applications/`.
