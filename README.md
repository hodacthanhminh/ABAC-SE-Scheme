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
docker build -f ${docker file} -t ${image_name} .
// run image
docker run -d --name ${container_name} -p ${publishPort}:${hostPort} ${image_name}
```
# Using docker compose
```
docker compose up
```

# .env needed 

```
ENDPOINT = '${CosmosDB Endpoint}'
KEY = '${API CosmosDB key}'
DATABASE_NAME = '${CosmosDB DatabaseName}'
INDEX_CONTAINER = '${Index container of DatabaseName}'
DOCUMENT_CONTAINER = '${Document container of DatabaseName}'
GPP_IP = 'http://localhost:8000/GPP'
AA1_IP = 'http://localhost:8081/abe'
AA2_IP = 'http://localhost:8082/abe'
AA3_IP = 'http://localhost:8083/abe'
SECRET = '${login Secret token}'
```

# link to ABE-AA 
https://github.com/minhhien2112/abe-aa


