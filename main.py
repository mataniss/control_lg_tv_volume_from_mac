import asyncio
import os
import json
import subprocess
from pynput import keyboard
from bscpylgtv import WebOsClient

TV_IP = "192.168.1.240"
client = None

def is_lg_display_connected():
    try:
        output = subprocess.check_output(["system_profiler", "SPDisplaysDataType"], text=True)
        return "LG" in output
    except Exception as e:
        print(f"[⚠️] Failed to check connected displays: {e}")
        return False

async def send_volume(direction):
    global client
    if not is_lg_display_connected():
        print("[🛑] No LG display detected. Volume command not sent.")
        return

    if client is None:
        await connect_to_tv()
    await client.connect()

    try:
        if direction == "up":
            await client.volume_up()
        elif direction == "down":
            await client.volume_down()
        print(f'sent {direction} action')
    except Exception as e:
        print(f"[❌] Failed to send volume command: {e}")

def on_press(key):
    try:
        if key == keyboard.Key.media_volume_up:
            asyncio.run(send_volume("up"))
        elif key == keyboard.Key.media_volume_down:
            asyncio.run(send_volume("down"))
    except Exception as e:
        print("[Error] Failed to send command:", e)

async def connect_to_tv():
    global client
    client = await WebOsClient.create(TV_IP, ping_interval=None, states=[])
    await client.connect()
    print("[✅] Connected and paired successfully.")

def main():
    print("[🖥] LG TV Volume Controller using aiopylgtv")
    asyncio.run(connect_to_tv())
    print("[🎧] Now listening for volume keys...")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
