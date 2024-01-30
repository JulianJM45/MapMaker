
from modules import createWebview


htmlfile = 'index.html'
cssfile = 'styles.css'
jsfile = 'scripts.js'


def main():
    createWebview(htmlfile, cssfile, jsfile)
    


if __name__ == '__main__':
    main()

