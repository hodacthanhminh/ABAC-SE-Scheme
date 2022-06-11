from azure.cosmos import CosmosClient, PartitionKey


class cosmos():
    def __init__(self,ep, k, db):
        self.client = CosmosClient(ep,k)
        self.database = self.client.create_database_if_not_exists(id=db)

    def setContainer(self, cn):
        self.container = self.database.create_container_if_not_exists(
            id = cn, partition_key=PartitionKey(path="/id"), offer_throughput=400
        )
        return self.container
    def createDocument(self,data):
        return self.container.create_item(body=data)
    
    def readDocument(self,id):
        return self.container.read_item(id,partition_key=id)

    def getContainer(self):
        return self.container
    
