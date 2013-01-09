# build
cp *.py ../dist/linux
cp autoexec.cfg ../ac_client/config/autoexec.cfg
cd ../dist/linux
ln -s jerboa_bin/jerboa jerboa
python bbfreeze_jerboa.py

# package
tar -zcvf jerboa.tar.gz jerboa_bin jerboa

# run
cp -a jerboa_bin jerboa ../../ac_client
cd ../../ac_client
mkdir jerboa_bin/jerboa_logs/past
cp -a jerboa_bin/jerboa_logs/*.txt jerboa_bin/jerboa_logs/past
./jerboa
