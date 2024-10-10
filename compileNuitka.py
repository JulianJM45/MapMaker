import subprocess


# Define the Nuitka command
command = [
    "nuitka",
    "--standalone",
    "--onefile",
    "--enable-plugin=pyqt5",
    "--include-data-dir=templates=templates",
    "--include-data-dir=static=static",
    "--include-data-file=icons/120px-Firepit.png=icons/120px-Firepit.png",  # Include the specific file
    "--include-data-file=modules/realesrgan-ncnn-vulkan=modules/realesrgan-ncnn-vulkan",  # Include the specific binary
    # "--include-data-file=modules/realesrgan-ncnn-vulkan.exe=modules/realesrgan-ncnn-vulkan.exe",  # for windows
    "--include-data-file=modules/models/realesrgan-x4plus.param=modules/models/realesrgan-x4plus.param",  # Include the model param file
    "--include-data-file=modules/models/realesrgan-x4plus.bin=modules/models/realesrgan-x4plus.bin",  # Include the model bin file
    "--output-dir=dist",
    "--output-filename=MapMaker_V3.1",
    # "--output-filename=MapMaker_V3.1.exe",  # for windows
    "main.py"
]

# Run the Nuitka command
subprocess.run(command, check=True)