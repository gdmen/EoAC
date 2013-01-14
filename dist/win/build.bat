copy ..\..\src\*.py .
setup.py py2exe
move setup.py ..\
del *.py
move ..\setup.py .
cd dist
del eoac.exe
ren jerboa.exe eoac.exe
cd ..