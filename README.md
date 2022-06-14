# Install charm-crypto and other packages following instruction

```
sudo apt-get install -y libgmp10 libgmp-dev
sudo apt-get install -y openssl

git clone https://github.com/JHUISI/charm

python3 -m venv venv
source ./venv/bin/activate

sudo ./install.sh
```


# Using docker 
```
docker build -t searchimage .

docker run -d --name mycontainer -p 80:80 searchimage
```


