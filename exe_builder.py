import subprocess
import os
import sys

def create_executable():
    # Path to the main.py file
    main_file = "main.py"

    # Check if main.py exists in the current directory
    if not os.path.isfile(main_file):
        print(f"Error: {main_file} not found in the current directory.")
        return

    # Find the path to PyInstaller
    def find_pyinstaller():
        for path in sys.path:
            possible_path = os.path.join(path, 'pyinstaller', 'cli.py')
            if os.path.isfile(possible_path):
                return possible_path
        return None

    pyinstaller_path = find_pyinstaller()
    if pyinstaller_path is None:
        print("Error: PyInstaller not found in sys.path")
        return

    # Command to run PyInstaller
    command = f"python {pyinstaller_path} --onefile {main_file}"

    try:
        # Run the command
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Print the output and any errors
        print("PyInstaller output:")
        print(process.stdout.decode())
        if process.stderr:
            print("PyInstaller errors:")
            print(process.stderr.decode())
    except subprocess.CalledProcessError as e:
        print("An error occurred while trying to create the executable:")
        print(e.output.decode())
        print(e.stderr.decode())

if __name__ == "__main__":
    create_executable()
