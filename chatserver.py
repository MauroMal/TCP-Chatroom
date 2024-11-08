import socket
import threading
from datetime import datetime
import os

# setup server
HOST = 'localhost'
PORT = 18000
MAX_USERS = 3
active_users = []
message_history = []

# handle client connections
def handle_client(conn, addr):
    global active_users
    username = None
    try:
        while True:
            message = conn.recv(4096).decode()
            if "JOIN_REQUEST_FLAG:1" in message:
                username = message.split('|')[1].split(':')[1]
                if len(active_users) >= MAX_USERS:
                    conn.send("JOIN_REJECT_FLAG:1|PAYLOAD:The chatroom has reached its maximum capacity.".encode())
                elif any(user['username'] == username for user in active_users):
                    conn.send("JOIN_REJECT_FLAG:1|PAYLOAD:Another user is using this username.".encode())
                else:
                    active_users.append({'username': username, 'conn': conn})
                    conn.send("JOIN_ACCEPT_FLAG:1".encode('utf-8'))
                    print(f"{username} has joined.")
                    announce = f"[{datetime.now().strftime('%H:%M:%S')}] Server: {username} joined the chatroom."
                    message_history.append(announce)
                    for user in active_users:
                        if user['conn'] != conn:
                            user['conn'].send(f"NEW_USER_FLAG:1|USERNAME:{username}|PAYLOAD:{announce}".encode())
                    conn.send("\n".join(message_history).encode())

            elif "ATTACHMENT_FLAG:1" in message:
                user = next((u for u in active_users if u['conn'] == conn), None)
                if user:
                    # extract the content from the message
                    content = message.split('|CONTENT:')[1].strip()
                    filename = message.split('|FILENAME:')[1].split('|CONTENT:')[0].strip()  # extract filename from the message
                    if content:

                        if not os.path.exists('downloads'):
                            os.makedirs('downloads')
                        with open(f'downloads/{filename}', 'w', encoding='utf-8') as f:
                            f.write(content)

                        msg = f"[{datetime.now().strftime('%H:%M:%S')}] {user['username']}: message: {content}"
                        message_history.append(msg)
            
            # broadcast the content to all connected users
                for u in active_users:
                    u['conn'].send(msg.encode('utf-8'))

            elif "REPORT_REQUEST_FLAG:1" in message:
                num_users = len(active_users)
                report = f"There are {num_users} active users in the chatroom.\n"
                report += "\n".join([f"{user['username']} at IP: {addr[0]} and port: {addr[1]}" for user in active_users])
                conn.send(f"REPORT_RESPONSE_FLAG:1|NUMBER:{num_users}|PAYLOAD:{report}".encode())
            
            elif "QUIT_REQUEST_FLAG:1" in message:
                user = next((u for u in active_users if u['conn'] == conn), None)
                if user:
                    active_users.remove(user)
                    quit_msg = f"[{datetime.now().strftime('%H:%M:%S')}] Server: {user['username']} left the chatroom."
                    message_history.append(quit_msg)
                    for u in active_users:
                        u['conn'].send(f"QUIT_ACCEPT_FLAG:1|USERNAME:{user['username']}|PAYLOAD:{quit_msg}".encode())
                break
            else:
                user = next((u for u in active_users if u['conn'] == conn), None)
                if user:
                    msg = f"[{datetime.now().strftime('%H:%M:%S')}] {user['username']}: {message}"
                    message_history.append(msg)
                    for u in active_users:
                        u['conn'].send(msg.encode())
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        if username:
            active_users = [user for user in active_users if user['username'] != username]
            quit_msg = f"[{datetime.now().strftime('%H:%M:%S')}] Server: {username} left the chatroom."
            print(quit_msg)
            message_history.append(quit_msg)
            for user in active_users:
                user['conn'].send(f"QUIT_ACCEPT_FLAG:1|USERNAME:{username}|PAYLOAD:{quit_msg}".encode())
        conn.close()

# server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(MAX_USERS)
print(f"Server running on {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
