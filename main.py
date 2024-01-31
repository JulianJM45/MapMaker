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

