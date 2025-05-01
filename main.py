import asyncio
import subprocess
from pynput import keyboard
from bscpylgtv import WebOsClient

TV_IP = "192.168.1.240"
client = None
is_muted = False

def is_lg_display_connected():
    try:
        output = subprocess.check_output(["system_profiler", "SPDisplaysDataType"], text=True)
        return "LG" in output
    except Exception as e:
        print(f"[⚠️] Failed to check connected displays: {e}")
        return False

async def connect_to_tv():
    global client
    if client is None:
        client = await WebOsClient.create(TV_IP, ping_interval=None, states=[])
    if not client.is_connected:
        await client.connect()
        print("[✅] Connected and paired successfully.")

async def send_volume(action):
    global client, is_muted

    if not is_lg_display_connected():
        print("[🛑] No LG display detected. Volume command not sent.")
        return

    try:
        await connect_to_tv()
        await client.connect()
        if action == "up":
            await client.volume_up()
        elif action == "down":
            await client.volume_down()
        elif action == "mute":
            is_muted = not is_muted
            await client.set_mute(is_muted)
            print(f"[🔇] Mute toggled: {'Muted' if is_muted else 'Unmuted'}")

        print(f"[📡] Sent '{action}' action")
    except Exception as e:
        print(f"[❌] Failed to send volume command: {e}")

def on_press(key):
    try:
        if key == keyboard.Key.media_volume_up:
            asyncio.run(send_volume("up"))
        elif key == keyboard.Key.media_volume_down:
            asyncio.run(send_volume("down"))
        elif key == keyboard.Key.media_volume_mute:
            asyncio.run(send_volume("mute"))
    except Exception as e:
        print("[Error] Failed to send command:", e)

def main():
    print("[🖥] LG TV Volume Controller using bscpylgtv")
    asyncio.run(connect_to_tv())
    print("[🎧] Now listening for volume keys...")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
