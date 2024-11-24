import subprocess
import os

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# List of scripts to run sequentially
scripts = [
    "1. Macro_RSS.py",
    "2. Media_RSS.py",
    "3. Filter_Media.py",
    "4. Combine.py",
    "5. Formatted Output.py"
]

# Run each script
for script in scripts:
    script_path = os.path.join(current_directory, script)  # Use absolute path to each script
    print(f"Running {script}...")
    try:
        # Run the script and wait for it to complete
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        print(f"{script} completed successfully.")
        print(result.stdout)  # Print the output of the script
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script}: {e}")
        print(e.stderr)  # Print the error output
        break  # Stop execution if a script fails
