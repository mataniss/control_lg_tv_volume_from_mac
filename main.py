import asyncio
import subprocess
import json
import threading
import requests
from pynput import keyboard
from bscpylgtv import WebOsClient
from wakeonlan import send_magic_packet
from aiohttp import web
from log import log

# Default fallback configuration
DEFAULT_CONFIG = {
    "tv_ip": "192.168.1.240",
    "tv_mac_address": "XX:XX:XX:XX:XX:XX",  # Replace with your TV's MAC address
    "lg_tv_volume_output_name": "LG TV",
    "server_port": 5001
}

# Load configuration from config.json
def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        log(f"[⚠️] Failed to load configuration: {e}")
        return None

# Apply configuration
config = load_config() or DEFAULT_CONFIG
TV_IP = config.get("tv_ip", DEFAULT_CONFIG["tv_ip"])
TV_MAC_ADDRESS = config.get("tv_mac_address", DEFAULT_CONFIG["tv_mac_address"])
LG_TV_VOLUME_OUTPUT_NAME = config.get("lg_tv_volume_output_name", DEFAULT_CONFIG["lg_tv_volume_output_name"])
SERVER_PORT = config.get("server_port", DEFAULT_CONFIG["server_port"])

client = None
is_muted = False
restart_listener_event = asyncio.Event()
listener_thread = None
listener_obj = None

def is_lg_audio_output():
    try:
        output = subprocess.check_output(["SwitchAudioSource", "-c"], text=True).strip()
        return LG_TV_VOLUME_OUTPUT_NAME in output
    except Exception as e:
        log(f"[⚠️] Failed to check audio output: {e}")
        return False

async def connect_to_tv():
    global client
    if client is None:
        client = await WebOsClient.create(TV_IP, ping_interval=None, states=[])
    if not client.is_connected:
        await client.connect()
        log("[✅] Connected and paired successfully.")

async def send_volume(action):
    global client, is_muted

    if not is_lg_audio_output():
        log("[🛑] No LG output detected. Volume command not sent.")
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
            log(f"[🔇] Mute toggled: {'Muted' if is_muted else 'Unmuted'}")

        log(f"[📡] Sent '{action}' action")

    except Exception as e:
        log(f"[❌] Failed to send volume command: {e}")
        log("[⚡] Sending WOL (Wake-on-LAN) packet to TV...")
        send_wol_packet()

def send_wol_packet():
    try:
        send_magic_packet(TV_MAC_ADDRESS)
        log(f"[🔋] WOL packet sent to MAC address: {TV_MAC_ADDRESS}")
    except Exception as e:
        log(f"[❌] Failed to send WOL packet: {e}")

def on_press(key):
    try:
        if "media_eject" in str(key):
            log("[⚡] Eject button pressed, sending WOL packet...")
            send_wol_packet()
            try:
                response = requests.get(f"http://localhost:{SERVER_PORT}/api/refreshKeysListener", timeout=2)
                log(f"[🌐] HTTP refresh triggered: {response.status_code}")
            except Exception as http_err:
                log(f"[❌] HTTP refresh error: {http_err}")
            return False

        elif key == keyboard.Key.media_volume_up:
            asyncio.run(send_volume("up"))
        elif key == keyboard.Key.media_volume_down:
            asyncio.run(send_volume("down"))
        elif key == keyboard.Key.media_volume_mute:
            asyncio.run(send_volume("mute"))

    except Exception as e:
        log("[Error] Failed to send command:", e)

def listen_once():
    global listener_thread, listener_obj

    def run():
        global listener_obj
        log("[🎧] Listening for volume keys... (Press Eject to restart)")
        with keyboard.Listener(on_press=on_press) as listener:
            listener_obj = listener
            listener.join()

    listener_thread = threading.Thread(target=run, daemon=True)
    listener_thread.start()

# ───────────── HTTP SERVER ─────────────

async def refresh_keys_listener(request):
    log("[🌐] /api/refreshKeysListener called, restarting listener...")
    if listener_obj:
        listener_obj.stop()
    restart_listener_event.set()
    return web.json_response({"status": "Listener restart triggered"})

async def start_http_server():
    app = web.Application()
    app.add_routes([web.get('/api/refreshKeysListener', refresh_keys_listener)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', SERVER_PORT)
    await site.start()
    log(f"[🌍] HTTP server running on port {SERVER_PORT}")

# ───────────── MAIN ─────────────

async def main_async():
    log("[🖥] LG TV Volume Controller using bscpylgtv")
    await connect_to_tv()
    asyncio.create_task(start_http_server())

    while True:
        restart_listener_event.clear()
        listen_once()
        await restart_listener_event.wait()

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
