# Creating Plugins for Raspberry Pi Light Web UI

This guide explains how to create, structure, and install plugins for the Raspberry Pi Light Web Interface.

## Plugin Structure
Every plugin must reside in its own folder within the `Plugins/` directory. The basic structure looks like this:

```text
Plugins/
└── MyPluginFolder/
    ├── plugin.json
    ├── index.html (or your main HTML file)
    └── assets/ (optional subfolders for CSS, JS, images)
```

## The plugin.json File
This is the core configuration file that tells the Web UI how to load your plugin. It must be a valid JSON file.

### Required Fields:
| Field | Description | Example |
| :--- | :--- | :--- |
| `name` | The display name of your plugin. | `"My Plugin"` |
| `path` | The URL path to the plugin's main HTML file. | `"/plugins/MyPluginFolder/index.html"` |
| `icon` | A FontAwesome icon name (omit the `fa-` prefix). | `"microchip"` (for `fa-microchip`) |

### Example `plugin.json`:
```json
{
  "name": "System Monitor",
  "path": "/plugins/SystemMonitor/monitor.html",
  "icon": "microchip"
}
```

## Adding Auth.js support
- For adding authentification to plugin using default JavaScript, add this to the start of your code:
```JavaScript
  <script src="/auth.js"></script>
```

## Execute shell commands using plugin
- To run shell commands using plugin add this JavaScript function to your HTML:
```JavaScript
function shellPlugin() {
	//Replace this with your shell command.
	const cmd = `echo "Hello, world!"`;
	
	try {
		const response = await fetch('/terminal/api', {
		method: 'POST',
		body: JSON.stringify({ command: cmd })
		});
			
		if (!response.ok) throw new Error("API Connection Failed");
}
```

## Installation & Management
- **Installing:** Unzip or move your plugin folder into the `Plugins/` directory of the project.
- **Enabling/Disabling:** Open the **Admin Panel**, scroll down to the **Plugin Manager**, and use the toggle buttons to manage your installed plugins.
- **Uninstalling:** Simply delete the plugin's folder from the `Plugins/` directory.
- Check [README](https://github.com/K3Soft-Hard/Raspberry-Pi---Light-Web-Interface?tab=readme-ov-file#raspberry-pi-light-web-interface) for more informations.

## Tips for Developers
- You can use subfolders within your plugin directory to organize scripts, styles, and images.
- Ensure the `path` in your `plugin.json` correctly reflects the folder name and the filename of your HTML page.
- Icons are pulled from FontAwesome; for example, if you want `fa-code`, just put `"code"` in the icon field.

## Addon Store

**Check out [Plugin Store](https://k3soft-hard.github.io/Rasberry-Pi---Web-Interface-STORE/)**
***Note: Only official plugins are available at this time.***