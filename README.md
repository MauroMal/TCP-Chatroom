<h1>Chatroom Application</h1>

<p>This project is a simple client-server chatroom application built using Python. It allows users to join a chatroom, exchange messages, share file attachments, and request a report of active users.</p>

<h2>Features</h2>
<ul>
    <li><strong>Client-Server Communication</strong>: Facilitates communication between multiple clients and a server using socket programming.</li>
    <li><strong>User Management</strong>: Users can join or leave the chatroom with unique usernames.</li>
    <li><strong>Message Broadcast</strong>: Messages sent by a user are broadcasted to all other active users.</li>
    <li><strong>File Sharing</strong>: Users can share text files with other participants.</li>
    <li><strong>Active User Report</strong>: Provides a report detailing the number of active users and their connection details.</li>
    <li><strong>Graphical User Interface (GUI)</strong>: The client side includes a user-friendly interface built with <code>tkinter</code>.</li>
</ul>

<h2>Project Structure</h2>
<ul>
    <li><strong>chatclient.py</strong>: The client-side application that includes a <code>tkinter</code>-based GUI for sending and receiving messages, uploading files, and interacting with the server.</li>
    <li><strong>chatserver.py</strong>: The server-side application that manages user connections, broadcasts messages, handles join/quit requests, and facilitates file sharing.</li>
</ul>

<h2>How to Run</h2>
<ol>
    <li><strong>Start the Server</strong>:
        <ul>
            <li>Run <code>chatserver.py</code> to start the server.</li>
            <li>The server will run on <code>localhost</code> and listen on port <code>18000</code> by default.</li>
        </ul>
        <pre><code>python chatserver.py</code></pre>
    </li>
    <li><strong>Run the Client</strong>:
        <ul>
            <li>Run <code>chatclient.py</code> to start a client instance.</li>
            <li>Connect to the server and interact through the GUI.</li>
        </ul>
        <pre><code>python chatclient.py</code></pre>
    </li>
</ol>

<h2>Usage</h2>
<ul>
    <li><strong>Joining the Chatroom</strong>: Enter a unique username when prompted.</li>
    <li><strong>Sending Messages</strong>: Type your message in the entry field and press "Send".</li>
    <li><strong>File Uploads</strong>: Click the <code>+</code> button to select and share a text file with all participants.</li>
    <li><strong>Requesting a Report</strong>: Use the "Menu" button to get a report of active users.</li>
    <li><strong>Exiting</strong>: Type <code>q</code> or use the menu to disconnect.</li>
</ul>

<h2>Requirements</h2>
<ul>
    <li>Python 3.12.3</li>
    <li><code>tkinter</code> for GUI support</li>
</ul>

<h2>Notes</h2>
<ul>
    <li>The server can handle a maximum of 3 simultaneous users as defined by <code>MAX_USERS</code>.</li>
    <li>File uploads are stored in a <code>downloads</code> directory on the server.</li>
    <li>The application currently supports text-based files for upload and display.</li>
</ul>

<h2>Author</h2>
<p>Mauro Malekshamran</p>
