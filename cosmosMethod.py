from azure.cosmos import CosmosClient, PartitionKey


class CosmosClass():
    def __init__(self, ep: str, k: str, db: str):
        self.client = CosmosClient(ep, k)
        self.database = self.client.create_database_if_not_exists(id=db)

    def set_container(self, cn: str):
        self.container = self.database.create_container_if_not_exists(
            id=cn, partition_key=PartitionKey(path="/id"), offer_throughput=400
        )
        return self.container

    def create_document(self, data):
        return self.container.create_item(body=data)

    def read_document(self, id: str):
        return self.container.read_item(id, partition_key=id)

    def get_container(self):
        return self.container

    def query_document_by_id(self, doc_id: str):
        return list(self.container.query_items(query="SELECT * FROM r WHERE r.id=@id",
                                               parameters=[
                                                   {"name": "@id", "value": doc_id}
                                               ],))
