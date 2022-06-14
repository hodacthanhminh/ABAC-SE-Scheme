pip install -r requirements.txt

cd charm

pip install pyparsing==2.4.6
pip install hypothesis
pip install pytest

./configure.sh
cd ./deps/pbc && make && ldconfig
cd - && make
make install && ldconfig
