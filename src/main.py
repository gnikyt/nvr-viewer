#!/usr/bin/env python3
import tkinter as tk
from tkinter.constants import BOTTOM, LEFT
import tkinter.simpledialog
import time
from urllib.request import urlopen
from PIL import ImageTk, Image, ImageDraw, ImageFont
from io import BytesIO
from os import environ, path
from math import floor
from subprocess import run


def resize_snapshot(img: Image) -> Image:
    """
        Resizes a snapshot to the window size while keeping aspect ratio.
    """

    # Get image size and window width
    width, height = img.size
    win_width = floor(window.winfo_width())

    # Horizontal layout, calculate number of cameras to fit inside window width
    new_width = win_width / channels_per_row
    new_width = floor(new_width)
    if new_width > 1:
        # new_width will be 1 or less if window is not truely open yet
        new_height = floor(new_width * (height / width))
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
    return img


def draw_info_snapshot(img: Image, channel: int) -> Image:
    """
        Add snapshot info.
    """

    # Get timestamp (24 hour) and text to overlay
    timestamp = time.strftime("%H:%M:%S")
    overlay_text = f"Channel {channel} / {timestamp}"

    # Set the font for the overlay text
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 10)

    # Draw the overlay text and rectangle
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle(((0, 00), (130, 20)), fill=(0, 0, 0, 200))
    draw.text((5, 5), overlay_text, fill=(255, 0, 0), font=fnt)
    return img


def get_snapshot(channel: int) -> ImageTk.PhotoImage:
    """
        Get a snapshot of a channel.
    """

    # Set the snapshot path
    data = None
    snapshot_path = f"http://{environ['NVR_IP']}/cgi-bin/snapshot.cgi?chn={channel}&u={environ['NVR_USERNAME']}&p={environ['NVR_PASSWORD']}"

    try:
        # Open the snapshot path, get the image data
        url = urlopen(snapshot_path)
        data = BytesIO(url.read())
        url.close()
    except Exception as e:
        # Network issue... happens sometimes when grabbing a snapshot
        data = open(path.join(path.dirname(__file__), "no-image.jpg"), "rb")

    # Assign into PIL, resize, and add text
    img = Image.open(data)
    img = resize_snapshot(img)
    img = draw_info_snapshot(img, channel)
    return ImageTk.PhotoImage(img)


def update_snapshots() -> None:
    """
        Update channel snapshots on screen.
    """

    for index, channel in enumerate(channels):
        img = get_snapshot(channel)
        if img is not False:
            clabels[index].configure(image=img)
            clabels[index].photo_ref = img


def snapshot_ticker() -> None:
    """
        Update the channel snapshots every 2 seconds.
    """

    update_snapshots()
    window.after(2000, snapshot_ticker)


# Create the window
title = "NVR Viewer"
window = tk.Tk(className="NVRViewer")
window.title(title)
window.configure(background="black")
window.geometry("800x800")

# Get the channel data and split channels into chunks of col/rows
channels = [int(channel) for channel in environ["NVR_CHANNELS"].split(",")]
channels_per_row = int(environ["NVR_CHANNELS_PER_ROW"])
channel_grid = (channels[i::channels_per_row] for i in range(channels_per_row))

# Create the channels in the view
clabels = []
for row, data in enumerate(channel_grid):
    for column, channel in enumerate(data):
        snapshot = get_snapshot(channel)
        label = tk.Label(window, image=snapshot)
        label.grid(row=row, column=column)
        clabels.append(label)

# Init loops
snapshot_ticker()
window.mainloop()
