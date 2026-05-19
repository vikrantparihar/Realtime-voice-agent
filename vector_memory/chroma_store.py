import chromadb

client = chromadb.Client()

collection = client.create_collection(name="bank_memory")

def save_memory(key, value):

    collection.add(
        documents=[value],
        ids=[key]
    )

def get_memory():

    results = collection.get()

    return results