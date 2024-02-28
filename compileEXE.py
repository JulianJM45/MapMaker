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
    "--name", "MyMakerV3",
    "--add-data", "index.html:.",
    "--add-data", "styles.css:.",
    "--add-data", "scripts.js:.",
    "--add-binary", f"modules/{executable}/:./modules",
    "--add-data", "modules/models:./modules/models",
    "main.py"
]

subprocess.run(command)

