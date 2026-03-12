# -*- coding: utf-8 -*-
import os, json, subprocess, time
from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
import datetime

HIDDEN_FILE = 'hidden_plugins.json'
LINKS_FILE = 'sidebar_links.json'
PORT = 8000

def get_hidden():
    try:
        with open('hidden_plugins.json', 'r') as f:
            return json.load(f)
    except:
        return

def save_hidden(hidden_list):
    with open(HIDDEN_FILE, 'w') as f: json.dump(hidden_list, f)

class MasterHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # 1. FIX SIDEBAR: Matches your HTML fetch('/api/files')
        if '/api/files' in self.path:
            exts = ('.txt', '.sh', '.py', '.html', '.css', '.json', '.js', '.mp3', '.wav')
            files_data = []
            for root, _, fs in os.walk("."):
                for f in fs:
                    if f.endswith(exts) and not f.startswith('.'):
                        path = os.path.relpath(os.path.join(root, f), ".")
                        files_data.append({"name": path}) # Must be a dict for f.name
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(files_data).encode())
            return

        elif '/api/stats' in self.path:
            stats = {"temp": "0", "mem": "0", "disk": "0"}
            try:
                # Direct hardware sensor read (Fixed Temperature)
                with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                    # The Pi stores temp as millidegrees (e.g., 45000)
                    temp_raw = f.read().strip()
                    stats["temp"] = str(round(int(temp_raw) / 1000, 1))
                
                # RAM Usage
                m = os.popen("free -m").read().splitlines()
                if len(m) > 1:
                    cells = m[1].split()
                    stats["mem"] = str(int((float(cells[2]) / float(cells[1])) * 100))

                # Disk Usage
                d = os.popen("df -h /").read().splitlines()
                if len(d) > 1:
                    stats["disk"] = d[1].split()[4].replace('%', '')

            except Exception as e:
                print(f"Stats error: {e}")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode())
            return

        # 3. PLUGIN ENGINE
        elif '/api/plugins' in self.path or '/api/all_plugins' in self.path:
            hidden = get_hidden()
            plugins = []
            if os.path.exists('./plugins'):
                for folder in os.listdir('./plugins'):
                    json_path = os.path.join('./plugins', folder, 'plugin.json')
                    if os.path.exists(json_path):
                        with open(json_path, 'r') as f:
                            data = json.load(f)
                            data['folder'] = folder
                            data['isHidden'] = folder in hidden
                            if '/api/plugins' in self.path and data['isHidden']: continue
                            plugins.append(data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(plugins).encode())
            return
        
        elif self.path == '/api/get_links':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if os.path.exists('sidebar_links.json'):
                with open('sidebar_links.json', 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"[]")
            return
        
        elif self.path == '/transfer':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('transfer.html', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        elif self.path == '/api/upload_history':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if os.path.exists('upload_history.json'):
                with open('upload_history.json', 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"[]")
            return

        # 4. HOME REDIRECT
        elif self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
            return

        return super().do_GET()

    def do_POST(self):
        
        content_length = int(self.headers.get('Content-Length', 0))

        if self.path == '/api/upload':
                    try:
                        content_length = int(self.headers.get('Content-Length', 0))
                        filename = self.headers.get('X-File-Name', 'unnamed_file')
                        folder_choice = self.headers.get('X-Folder', 'Main')
                        
                        print(f"--- Uploading: {filename} to {folder_choice} ---")

                        # Define absolute path to be safe
                        base_dir = './'
                        
                        paths = {
                            "Main": base_dir,
                            "Plugins": os.path.join(base_dir, "plugins"),
                            "Video": os.path.join(base_dir, "video"),
                            "Photo": os.path.join(base_dir, "photo"),
                            "Music": os.path.join(base_dir, "music")
                        }
                        
                        target_path = paths.get(folder_choice, base_dir)

                        # Create folder if missing
                        if not os.path.exists(target_path):
                            print(f"Creating folder: {target_path}")
                            os.makedirs(target_path, exist_ok=True)

                        save_file_path = os.path.join(target_path, filename)

                        # READ BINARY DATA
                        file_data = self.rfile.read(content_length)
                        
                        with open(save_file_path, 'wb') as f:
                            f.write(file_data)
                        
                        print(f"Successfully saved to: {save_file_path}")

                        # History logic (simplified to prevent errors)
                        try:
                            import datetime
                            history_file = os.path.join(base_dir, 'upload_history.json')
                            history = []
                            if os.path.exists(history_file):
                                with open(history_file, 'r') as f:
                                    history = json.load(f)
                            history.insert(0, {"name": filename, "date": datetime.datetime.now().strftime("%H:%M:%S"), "folder": folder_choice})
                            with open(history_file, 'w') as f:
                                json.dump(history[:10], f)
                        except Exception as e:
                            print(f"History Error: {e}")

                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'{"status":"success"}')
                        return

                    except Exception as e:
                        print(f"FATAL UPLOAD ERROR: {e}")
                        self.send_response(500)
                        self.end_headers()
                        return
        
        # READ DATA ONCE (Crucial: reading twice crashes the server)
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        try:
            data = json.loads(body)
        except:
            data = {}

        if self.path == '/api/save_links':
            with open('sidebar_links.json', 'w') as f:
                json.dump(data, f, indent=4)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return  # <--- THIS STOPS THE CRASH. It exits before line 119.     

        # 1. SAVE (Triggers the alert dialog)
        if '/save' in self.path:
            filename = data.get('filename')
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(data.get('content', ''))
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
            return

        elif '/run' in self.path:
                # The browser needs these 2 lines IMMEDIATELY 
                # to prevent "Failed to fetch"
                self.send_response(200)
                self.end_headers()
                
                # Now do the work
                filename = data.get('filename')
                os.system(f"chmod +x {filename}")
                os.system(f"./{filename} > output.txt 2>&1")
                
                # Send the answer
                with open("output.txt", "r") as f:
                    self.wfile.write(f.read().encode())
                return

        # 3. TERMINAL
        elif '/terminal/api' in self.path:
            cmd = data.get('command', '')
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            self.send_response(200); self.end_headers()
            self.wfile.write((res.stdout + res.stderr).encode())
            return
        
        elif '/api/toggle_plugin' in self.path:
            folder = data.get('folder') # This is the folder name of the plugin
            hidden = get_hidden()       # Loads the current list of hidden ones
            
            if folder in hidden:
                hidden.remove(folder)   # Make it visible
            else:
                hidden.append(folder)   # Hide it
            
            save_hidden(hidden)         # Writes it back to hidden_plugins.json
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"success"}')
            return
        
        elif self.path == '/api/new_document':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            filename = data.get('filename', 'untitled.py')
            
            # Create the file in the current directory
            try:
                with open(filename, 'w') as f:
                    f.write("") # Create an empty file
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())

if __name__ == '__main__':
    print("--- SERVER FULLY REPAIRED ---")
    # HTTPServer(('0.0.0.0', PORT), MasterHandler).serve_forever()
    ThreadingHTTPServer(('0.0.0.0', PORT), MasterHandler).serve_forever()
