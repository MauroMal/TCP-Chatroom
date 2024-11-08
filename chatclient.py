import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog, simpledialog, messagebox
from PIL import Image, ImageTk  # for displaying image attachments
import os
import io
import base64

# connects to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = 'localhost'
port = 18000
client_socket.connect((server_host, port))

# display menu and handle user choices
def show_menu():
    choice = simpledialog.askinteger("Menu", "Select an option:\n1. Get a report of the chatroom.\n2. Request to join the chatroom.\n3. Quit the program.")
    if choice == 1:
        client_socket.send("REPORT_REQUEST_FLAG:1".encode())
    elif choice == 2:
        username = simpledialog.askstring("Join Chatroom", "Please enter a username:")
        if username:
            join_request = f"JOIN_REQUEST_FLAG:1|USERNAME:{username}"
            client_socket.send(join_request.encode())
    elif choice == 3:
        client_socket.send("QUIT_REQUEST_FLAG:1".encode())
        client_socket.close()
        root.quit()
    else:
        messagebox.showinfo("Invalid Choice", "Please select a valid option (1, 2, or 3).")


# receive messages from the server
def receive_messages():
    while True:
        try:
            # read the initial message or header from the server and decode
            header = client_socket.recv(1024).decode()
            chat_display.config(state='normal')
            chat_display.insert(tk.END, header + '\n')
            chat_display.config(state='disabled')
            chat_display.see(tk.END)
        except Exception as e:
            print("Error receiving message:", e)
            break


# function to send messages to the server
def send_message():
    message = message_entry.get()
    if message.strip():
        client_socket.send(message.encode())
        if message.lower() == 'q':
            client_socket.send("QUIT_REQUEST_FLAG:1".encode())
            client_socket.close()
            root.quit()
        message_entry.delete(0, tk.END)

# function to upload files
def upload_file():
    filepath = filedialog.askopenfilename(title="Select a file")
    if filepath:
        filename = os.path.basename(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()

        # s a message with both the filename and the content
        client_socket.send(f"ATTACHMENT_FLAG:1|FILENAME:{filename}|CONTENT:{file_content}".encode('utf-8'))



# GUI with tkinter
root = tk.Tk()
root.title("Chatroom Client")

menu_button = tk.Button(root, text="Menu", command=show_menu)
menu_button.pack(pady=5)

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state='disabled')
chat_display.pack(padx=5, pady=5)

plus_button = tk.Button(root, text="+", command=upload_file)
plus_button.pack(side="left", padx=5)

message_entry = tk.Entry(root, width=40)
message_entry.pack(side='left')

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side='right', padx=5)

# start receiving thread
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()