import os
import ast
import time
import random
import platform
import requests
import subprocess
import tkinter as tk
from cffi import FFI
from math import pi, cos, sin
from dotenv import load_dotenv

ffi = FFI()

#C code to define function signatures
ffi.cdef("""
    double calculate_new_angle(double current_angle, double angle_step);
    void calculate_wedge_positions(double wheel_radius, double center_x, double center_y, double angle, double angle_step, double* positions);
    double slow_down(double speed, double factor);
    int generate_random_color();
""")

# Load API key
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv()

# Fetch SteamAPI, STEAM_IDS, and API URL from env
api_key = os.environ.get("API_KEY")
api_url = os.environ.get("API_URL")
steam_id_str = ast.literal_eval(os.environ.get("STEAM_IDS"))
steam_ids = list(steam_id_str.values())[0:]

# Error handling if values aren't set
if (api_key or steam_ids) is None:
    raise ValueError("Value not found, please set it in the .env file.")

# Get games for single steam ID
def get_owned_games(api_key, steam_id):
    """Fetching owned games from Steam API."""
    params = {
        'key': api_key,
        'steamid': steam_id,
        'include_appinfo': True,
        'include_played_free_games': True
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    games = data['response'].get('games', [])
    return games

def get_shared_games(api_key, steam_ids):
    """Fetching owned games for multiple Steam users."""
    all_games = []
    for steam_id in steam_ids:
        games = get_owned_games(api_key, steam_id)
        game_set = set(game['appid'] for game in games)
        all_games.append(game_set)

    # Find the intersection of all sets
    shared_game_ids = set.intersection(*all_games)

    # Convert back to list of games with names
    shared_games = []
    for steam_id in steam_ids:
        for game in games:
            if game['appid'] in shared_game_ids:
                shared_games.append({'name': game['name'], 'appid': game['appid']})
        break   # Only need the names once since they're shared among all users
    return shared_games

class GameWheelApp:
    def __init__(self, root, games):
        self.root = root
        self.games = games
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        # Wheel properties
        self.wheel_center = (200, 200)
        self.wheel_radius = 150
        self.angle_step = 2 * pi / len(self.games)
        self.current_angle = 0

        # Create the wheel
        self.create_wheel()

        # Create a button to start the wheel
        self.start_button = tk.Button(root, text="Spin the Wheel!", command=self.spin_wheel)
        self.start_button.pack()

        # Flag to check if wheel is spinning
        self.is_spinning = False

    def create_wheel(self):
        """Draw the game wheel with game names."""
        self.wedges = []
        self.canvas.delete("all")

        for i, game in enumerate(self.games):
            angle = self.current_angle + i * self.angle_step

            # Call the C function to get wedge positions
            positions = ffi.new("double[4]")
            C.calculate_wedge_positions(self.wheel_radius, self.wheel_center[0], self.wheel_center[1], angle, self.angle_step, positions)
            
            x1, y1, x2, y2 = positions[0], positions[1], positions[2], positions[3]

            # Draw the wedge
            wedge = self.canvas.create_polygon(
                self.wheel_center[0], self.wheel_center[1], x1, y1, x2, y2,
                fill=self.random_color(), outline="black")

            # Place the game name
            text_angle = angle + self.angle_step / 2
            text_x = self.wheel_center[0] + (self.wheel_radius * 0.7) * cos(text_angle)
            text_y = self.wheel_center[1] + (self.wheel_radius * 0.7) * sin(text_angle)
            self.canvas.create_text(text_x, text_y, text=game['name'], angle=0)

    def random_color(self):
        """Return a random color."""
        return "#%06x" % C.generate_random_color()
    
    def spin_wheel(self):
        """Spin the wheel and slow down until it lands on a game."""
        if self.is_spinning:
            return
        self.is_spinning = True

        # Set random number of rotations and the final game it will land on
        total_spins = random.randint(8,10)
        slowing_factor = 1.05   # Will increase to slow down the wheel
        speed = 0.1             # Initial speed of rotation
        final_game_index = random.randint(0, len(self.games) - 1)

        # Animation loop
        def spin():
            nonlocal total_spins, speed, slowing_factor, final_game_index
            if total_spins > 0 or speed > 0.2:
                # Call the C function to update the angle
                self.current_angle = C.calculate_new_angle(self.current_angle, self.angle_step)
                self.create_wheel()     # Redraw the wheel at the new angle

                total_spins -= 1
                speed = C.slow_down(speed, slowing_factor)     # Gradually slow down using C function
                self.root.after(int(speed * 100), spin) # Continue spinning
            else:
                # Stop spinning and highlight the final game
                self.is_spinning = False
                print(f"Landed on: {self.games[final_game_index]['name']}")
        spin()

# Main program
def main():
    global C
    # Compile and load the shared library
    if platform.system() == 'Windows':
        dllPath = os.path.join(os.path.dirname(__file__), 'wheel.dll')
        if os.path.exists(dllPath):
            pass
        else:
            cPath = os.path.join(os.path.dirname(__file__), 'wheel.c')
            compile_command = f"gcc -shared -o {dllPath} -fPIC {cPath}"
            subprocess.run(compile_command, shell=True)
            time.sleep(4)
        C = ffi.dlopen(dllPath)
    elif (platform.system() == 'Linux' or platform.system() == 'Darwin'):
        soPath = os.path.join(os.path.dirname(__file__), 'wheel.so')
        if os.path.exists(soPath):
            pass
        else:
            cPath = os.path.join(os.path.dirname(__file__), 'wheel.c')
            compile_command = f"gcc -shared -o {soPath} -fPIC {cPath} -lm"
            subprocess.run(compile_command, shell=True)
            time.sleep(4)
        C = ffi.dlopen(soPath)

    # Fetch shared games among the Steam IDs
    shared_games = get_shared_games(api_key, steam_ids)

    # Filter and prepare game names
    if shared_games:
        game_names = [{'name': game['name']} for game in shared_games]
    else:
        game_names = [{'name': 'No owned games found.'}]

    # Set up the GUI
    root = tk.Tk()
    app = GameWheelApp(root, game_names)
    root.mainloop()

if __name__ == "__main__":
    main()