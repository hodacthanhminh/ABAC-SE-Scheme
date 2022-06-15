# Experimental Environment
`Kernel` : Linux 
`Python` : Version 3.7.13
# Install charm-crypto and other packages following instruction
```
// system lib required
sudo apt-get install flex bison m4
sudo apt-get install libssl-dev
sudo apt-get install -y libgmp10 libgmp-dev
sudo apt-get install -y openssl

git clone https://github.com/JHUISI/charm

python3 -m venv venv
source ./venv/bin/activate

sudo ./install.sh
```


# Using docker 
```
// build image
docker build -t ${image_name} .
// run image
docker run -d --name ${container_name} -p 80:80 ${image_name}
```


