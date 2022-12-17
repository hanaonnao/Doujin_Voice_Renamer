import PyInstaller.__main__


PyInstaller.__main__.run([
    'dlsite_renamer.py',
    '--onefile',
    '--windowed',
    '--clean',
    '--icon',
    'favicon_128x128.ico',
])
