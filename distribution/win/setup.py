from distutils.core import setup
import py2exe

setup(
    console=['../../jerboa.py'], # list of scripts to convert into console exes 
    zipfile=None, # library files in exe instead of zipfile (defaults to "library.zip")
    options = {
        'py2exe': {
            'bundle_files': 1, # bundle dlls and python interpreter in the exe
         }
    }
)
