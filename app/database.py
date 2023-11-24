from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def get_cassandra_session():
    auth_provider = PlainTextAuthProvider(username='your_username', password='your_password')
    cluster = Cluster(['cassandra_host'], auth_provider=auth_provider)
    session = cluster.connect()
    session.set_keyspace('your_keyspace')
    return session

# Example function to insert data
def insert_image_data(session, image_id, image_data):
    cql = "INSERT INTO your_table (image_id, data) VALUES (%s, %s)"
    session.execute(cql, (image_id, image_data))
