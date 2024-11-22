import subprocess

# List of scripts
scripts = ["1.Macro_RSS.py", "2.Media_RSS.py", "3.Filter_Media.py"]

# Run scripts in the same interpreter PyCharm uses
interpreter = "/path/to/venv/bin/python"  # Replace with your PyCharm Python interpreter

for script in scripts:
    print(f"Running {script}...")
    try:
        subprocess.run([interpreter, script], check=True)
        print(f"Finished running {script}\n")
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script}: {e}")
        break
