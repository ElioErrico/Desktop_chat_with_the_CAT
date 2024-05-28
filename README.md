
# Desktop Chat with Cheshire Cat

This program creates a desktop chat application to communicate with the Cheshire Cat using its API.

## Features

0) Set the Host, Default is local host
1) Desktop Interface: A chat GUI built with Tkinter.
2) Cheshire Cat API: Interacts with the Cheshire Cat API to send and receive messages.
3) Automatic User ID: The user is automatically created using the computer's name.
4) Message Display Mode: Choose between token-by-token message streaming or direct final output.

## Setting Message Display Mode

Modify the following line to set the message display mode:
self.chat_type = "chat"
Set self.chat_type to "chat_token" for token-by-token message streaming.

## Creating an Executable

To create an executable (.exe) file, use pyinstaller run: exe_builder.py


![image](https://github.com/ElioErrico/Desktop_chat_with_the_CAT/assets/143315119/c5cff691-4548-4eee-83ba-748cc184cfc7)
