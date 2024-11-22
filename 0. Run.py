import subprocess
import os

# Directory where the scripts are located
script_dir = "/Users/rodrigo.varela/PycharmProjects/RWA-media/"

# List of scripts to run in order
scripts = [
    "1.Macro_RSS.py",
    "2.Media_RSS.py",
    "3.Filter_Media.py"
]

# Execute each script in the defined order
for script in scripts:
    script_path = os.path.join(script_dir, script)
    print(f"Running {script_path}...")
    try:
        subprocess.run(["python", script_path], check=True)
        print(f"Finished running {script}\n")
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script}: {e}")
        break
