
FOLDER=$(python -c "import os; print(os.path.dirname(os.path.realpath('$0')))")
cd $FOLDER

yes | pip3 install picamera

sudo pip install --upgrade git+https://github.com/Maratyszcza/PeachPy
sudo pip install --upgrade git+https://github.com/Maratyszcza/confu

git clone https://github.com/ninja-build/ninja.git
cd ninja
git checkout release
./configure.py --bootstrap
export NINJA_PATH=$PWD
cd ..


git clone https://github.com/shizukachan/NNPACK
cd NNPACK
confu setup
python ./configure.py --backend auto

$NINJA_PATH/ninja
sudo cp -a lib/* /usr/lib/
sudo cp include/nnpack.h /usr/include/
sudo cp deps/pthreadpool/include/pthreadpool.h /usr/include/
cd ..

make
