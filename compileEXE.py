import subprocess
import platform

if platform.system() == 'Windows':
    executable = 'realesrgan-ncnn-vulkan.exe'
elif platform.system() == 'Linux':
    executable = 'realesrgan-ncnn-vulkan'
elif platform.system() == 'Darwin':
    executable = 'realesrgan-ncnn-vulkan'
else:
    print('Unknown OS')

command = [
    "pyinstaller",
    "--onefile",
    "--console",
    "--name", "MapMakerV4",
    "--add-data", "templates/index.html:./templates",
    "--add-data", "static/styles.css:./static",
    "--add-data", "static/scripts.js:./static",
    "--add-data", "app.py:.",
    "--add-binary", f"modules/{executable}/:./modules",
    "--add-binary", "/usr/lib/x86_64-linux-gnu/libpython3.12.so:./",  # Add Python shared library
    "--add-data", "modules/models:./modules/models",
    "main.py"
]

subprocess.run(command)


## search libpython3.12.so
# find /usr -name "libpython3.12.so"