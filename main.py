#!/usr/bin/env python3
import tkinter as tk
import time
from urllib.request import urlopen
from PIL import ImageTk, Image, ImageDraw, ImageFont
from io import BytesIO
from os import environ
from typing import Union
from math import floor


def resize_snapshot(img: Image) -> Image:
    """
        Resizes a snapshot to the window size while keeping aspect ratio.
    """

    width, height = img.size
    new_width = floor(window.winfo_width())
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


def get_snapshot(channel: int) -> Union[ImageTk.PhotoImage, bool]:
    """
        Get a snapshot of a channel.
    """

    snapshot_path = f"http://{environ['NVR_IP']}/cgi-bin/snapshot.cgi?chn={channel}&u={environ['NVR_USERNAME']}&p={environ['NVR_PASSWORD']}"
    try:
        # Open the snapshot path, get the image data
        url = urlopen(snapshot_path)
        data = BytesIO(url.read())
        url.close()

        # Assign into PIL, resize, and add text
        img = Image.open(data)
        img = resize_snapshot(img)
        img = draw_info_snapshot(img, channel)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error getting snapshot for channel {channel}... {str(e)}")
        return False


def update_snapshots() -> None:
    """
        Update channel snapshots on screen.
    """

    for channel in range(len(clabels)):
        img = get_snapshot(channel)
        if img is not False:
            clabels[channel].configure(image=img)
            clabels[channel].photo_ref = img


def snapshot_ticker() -> None:
    """
        Update the channel snapshots every 2 seconds.
    """

    update_snapshots()
    window.after(2000, snapshot_ticker)


# Create the window
window = tk.Tk()
window.configure(background="black")
window.title("NVR Viewer")

# Create the labels for each channel 
clabels = []
for channel in range(0, int(environ['NVR_CHANNELS'])):
    snapshot = get_snapshot(channel)
    label = tk.Label(window, image=snapshot)
    label.pack()
    clabels.append(label)

# Init loops
snapshot_ticker()
window.mainloop()
