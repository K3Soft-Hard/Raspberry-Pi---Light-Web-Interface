# Rasberry-Pi Light Web Interface
It has a lot of bugs that I want to fix in the future.
The code is very messy. Feel free to download it and change the code.
I tried to comment every change that I did.
### This is a small web interface with built-in:
  - Editor from HTML, SCRIPTS, PYTHON and JSON
  - Admin panel with temperature, storage and memory
  - Music player
  - Video player
  - Photo Viewer
  - Plugin manager for installing plugins
  - Home screen

### Other features:
  - Web Terminal (beta)
  - Option to make host site on local network
  - [Password for UI](### Password Lock)

### Local site hosting
Open editor and click "New Document" enter name of your document.html. Now you can make your code and then click "SAVE" and exit editor. On main screen press "+" in bottom bar and add enter name of your shortcut and path to your site (ex. document.html). Now when you click that shortcut your site will open. You can delete shortcut by clicking trash icon next to your shortcut

### Password Lock
This password is not secure and can be easily bypassed, so don't rely on it. To configure password you need to change <br> **auth-config.json** in editor: <br>
`{
  "auth_enabled": false,
  "password": "secret"
}`