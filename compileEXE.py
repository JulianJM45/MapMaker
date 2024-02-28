import subprocess

command = [
    "pyinstaller",
    "--onefile",
    "--console",
    "--name", "MyMakerV3",
    "--add-data", "index.html:.",
    "--add-data", "styles.css:.",
    "--add-data", "scripts.js:.",
    "--add-binary", "modules/realesrgan-ncnn-vulkan:./modules",
    "--add-data", "modules/models:./modules/models",
    "main.py"
]

subprocess.run(command)

