# Install charm-crypto following

sudo apt-get install -y libgmp10 libgmp-dev
sudo apt-get install -y openssl

git clone https://github.com/JHUISI/charm

python3 -m venv venv
source ./venv/bin/activate

sudo ./install.sh



