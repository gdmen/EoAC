from cx_Freeze import setup,Executable

includefiles = ['README.txt', 'CHANGELOG.txt', 'helpers\uncompress\unRAR.exe', , 'helpers\uncompress\unzip.exe']
includes = []
excludes = ['Tkinter']
packages = ['do','khh']

setup(
    name = 'myapp',
    version = '0.1',
    description = 'A general enhancement utility',
    author = 'lenin',
    author_email = 'le...@null.com',
    options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}}, 
    executables = [Executable('janitor.py')]
)
