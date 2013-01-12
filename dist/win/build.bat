copy ..\..\src\*.py .
setup.py py2exe
move setup.py ..\
del *.py
move ..\setup.py .