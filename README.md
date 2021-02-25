# NVR Viewer

My NVR system uses Flash for web display. Now that Flash is disabled, I needed a way to casually view my cameras from my desktop.

This is a simple script which uses TKinter and PIL to grab each channel's image snapshot and display it (stacked).

The snapshots resize to the window's size and overlays the current time.

Each snapshot will update every two seconds.

## Installation

Requires Python 3.6 or higher, PIL, and TKinter

Once installed, copy rename `nvr-viewer.desktop.dist` to `nvr-viewer.desktop`.

Fill in the environment variables for username, password, IP, and channels.

Move or symlink the desktop file `~/.local/share/applications/`.
