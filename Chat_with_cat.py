import tkinter as tk
from tkinter import scrolledtext
#######
from ttkthemes import ThemedTk ##### aggiunta libreria
from tkinter import ttk ##### aggiunta libreria
#######
import time
import cheshire_cat_api as ccat
import json
from cheshire_cat_api.api_client import ApiClient
from cheshire_cat_api.configuration import Configuration
from cheshire_cat_api.api.memory_api import MemoryApi   # Assicurati che il percorso di importazione sia corretto
import platform

class APIClient:
    def __init__(self, user_id, base_url="localhost", port=1865, auth_key="", secure_connection=False, on_message_callback=None):
        self.config = ccat.Config(
            user_id=user_id,
            base_url=base_url,
            port=port,
            auth_key=auth_key,
            secure_connection=secure_connection,
        )
        self.cat_client = ccat.CatClient(config=self.config, on_message=on_message_callback)
        
        # Configurazione dell'ApiClient con le stesse impostazioni
        scheme = "https" if secure_connection else "http"
        api_config = Configuration(
            host=f"{scheme}://{base_url}:{port}",
            api_key={'Authorization': auth_key}
        )
        
        self.memory_api = MemoryApi(api_client=ApiClient(configuration=api_config))
    
    def connect(self):
        self.cat_client.connect_ws()
        while not self.cat_client.is_ws_connected:
            time.sleep(1)
    
    def send_message(self, message):
        self.cat_client.send(message=message)
    
    def close_connection(self):
        self.cat_client.close()
    
    def wipe_chat_history(self):
        try:
            response = self.memory_api.wipe_conversation_history(_headers={"user_id":self.config.user_id})
            return response
        except Exception as e:
            print(f"Error wiping chat history: {e}")
            return None

class ChatApp:
    def __init__(self, root, api_client):
        self.root = root
        self.root.title("Chat")

        ####
        self.font = ("Segoe UI", 12) #### Aggiunto Font
        ####

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', font=self.font)  ##### inserito font
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ######
        self.entry = ttk.Entry(root, font=self.font) ##### inserito font
        ######
        self.entry.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.entry.bind("<Return>", self.send_message)
        
        self.api_client = api_client
        self.api_client.connect()

        self.bot_message = ""  # Variable to accumulate bot messages
        self.bot_message_id = None  # Variable to keep track of the bot message line
        self.receiving_tokens = False  # Initialize receiving_tokens

        # Add the clear chat button
        ######
        self.clear_button = ttk.Button(root, text="Elimina chat", command=self.clear_chat, style="TButton") #### aggiunto ttk button
        ######
        self.clear_button.pack(padx=10, pady=(0, 10))

        self.style = ttk.Style() #### aggiunto ttk button
        self.style.configure("TButton", font=self.font) #### aggiunto ttk button

    def send_message(self, event=None):
        user_message = self.entry.get()
        if user_message:
            self.entry.delete(0, tk.END)
            self.display_message("You", user_message,"#2f4f4f")  ####### inserito colore
            self.api_client.send_message(user_message)
            self.receiving_tokens=False
    
    def display_message(self, sender, message, color):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n",(color)) ########## aggiunto colore
        self.chat_area.tag_config(color, foreground=color) ########## aggiunto colore
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def update_bot_message(self, content):
        
        self.chat_area.configure(state='normal') 
        
        if self.receiving_tokens == True: 
            self.receiving_tokens=not self.receiving_tokens
            print(self.receiving_tokens)
            self.bot_message = content 
            self.bot_message_id = self.chat_area.index(tk.END + "-1c")
            self.chat_area.insert(tk.END, f"Bot: {self.bot_message}\n", ("#191970"))  ########## aggiunto colore
        else:
            print(self.receiving_tokens)
            self.bot_message += content 
            self.chat_area.delete(f"{self.bot_message_id} linestart", f"{self.bot_message_id} lineend") 
            self.chat_area.insert(self.bot_message_id, f"Bot: {self.bot_message}", ("#191970"))  ########## aggiunto colore
        
        self.chat_area.tag_config("#191970", foreground="#191970")  ########## aggiunto colore
        self.chat_area.configure(state='disabled') 
        self.chat_area.see(tk.END)


    def clear_chat(self):
        response = self.api_client.wipe_chat_history() 
        if response:
            self.chat_area.configure(state='normal')
            self.chat_area.delete(1.0, tk.END)
            self.chat_area.configure(state='disabled')
            self.bot_message = ""
            self.bot_message_id = None
        else:
            print("Failed to wipe chat history.")

    def close(self):
        self.api_client.close_connection()
        self.root.destroy()

    def on_message_from_api(self, message):
        data = json.loads(message)
        if data.get("type") == "chat_token":
            content = data.get("content", "")
            if content:
                self.update_bot_message(content)
                print(content)
            else:
                self.receiving_tokens = not self.receiving_tokens
                print(self.receiving_tokens)


########### AGGIUINTA FUNZIONE CHE LEGGE IL PC ##########
def get_computer_name_platform():
    try:
        computer_name = platform.node()
        return computer_name
    except Exception as e:
        return str(e)
####################################   

if __name__ == "__main__":
    #####
    root = ThemedTk(theme="adapta")  # Imposta il tema qui
    ####
    api_client = APIClient(user_id=get_computer_name_platform(), on_message_callback=lambda message: app.on_message_from_api(message)) ########### INSERITA FUNZIONE CHE LEGGE IL PC
    app = ChatApp(root, api_client)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()

    
