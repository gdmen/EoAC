cp ../jerboa.py win/jerboa.py
cp ../constants.py win/constants.py
cd win
setup.py py2exe
cd ..