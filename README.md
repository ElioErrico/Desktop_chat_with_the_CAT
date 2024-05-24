
# Desktop Chat with Cheshire Cat

This program creates a desktop chat application to communicate with the Cheshire Cat using its API.

## Features

Desktop Interface: A chat GUI built with Tkinter.
Cheshire Cat API: Interacts with the Cheshire Cat API to send and receive messages.
Automatic User ID: The user is automatically created using the computer's name.
Message Display Mode: Choose between token-by-token message streaming or direct final output.
Configuration
Dependencies
Ensure you have the following dependencies installed:

## Setting Message Display Mode

Modify the following line to set the message display mode:
self.chat_type = "chat"
Set self.chat_type to "chat_token" for token-by-token message streaming.

## Creating an Executable

To create an executable (.exe) file, use pyinstaller:
Install pyinstaller
Generate the .exe  with pyinstaller --onefile main.py
The executable will be located in the dist folder within your project directory.
