import os
from modules import createWebview


# htmlfile = 'index.html'
# cssfile = 'styles.css'
# jsfile = 'scripts.js'

# Get the directory of the current script or executable
current_dir = os.path.dirname(os.path.realpath(__file__))

htmlfile = os.path.join(current_dir, 'index.html')
cssfile = os.path.join(current_dir, 'styles.css')
jsfile = os.path.join(current_dir, 'scripts.js')


def main():
    createWebview(htmlfile, cssfile, jsfile)
    

if __name__ == '__main__':
    main()


# pyinstaller --onefile --console --name MyMakerV4 --add-data 'index.html:.' --add-data 'styles.css:.' --add-data 'scripts.js:.' --add-binary 'modules/realesrgan-ncnn-vulkan:modules' --add-data 'modules/models:modules' main.py
# Note: If you're on Windows, replace the colons (:) in the --add-data options with semicolons (;).