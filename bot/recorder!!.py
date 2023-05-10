import asyncio
import websockets
import time
import pyautogui
import cv2
import numpy as np
import os

async def handler(websocket, path):
    recording = False
    async for message in websocket:
        print(f"Received message: {message}")
        if message.strip() == "3131" and not recording:
            # set up video recording parameters
            resolution = pyautogui.size()
            codec = cv2.VideoWriterfourcc(*"mp4v")
            timestamp = int(time.time())
            filename = f"video{timestamp}.mp4"
            # create "records" folder if it doesn't exist
            if not os.path.exists("records"):
                os.makedirs("records")
            # create video file in "records" folder
            filepath = os.path.join("records", filename)
            out = cv2.VideoWriter(filepath, codec, 15.0, resolution)
            recording = True
            print("recording started")
            # start recording video
            while recording:
                # take a screenshot and convert it to an OpenCV image
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # write the frame to the video file
                out.write(frame)
                # stop recording after 7 seconds
                if time.time() - timestamp >= 10:
                    recording = False
            out.release()
            print("recording ended")

async def main():
    async with websockets.serve(handler, "localhost", 3131):
        print("WebSocket server started")
        while True:
            await asyncio.sleep(1)

asyncio.run(main())