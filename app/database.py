from cassandra.cluster import Cluster

def get_cassandra_session():
    cluster = Cluster(['cassandra'])  # Since both are on the same Docker network
    session = cluster.connect()
    session.set_keyspace('botaniqai')
    return session

def insert_image_data(session, image_id, image_data):
    cql = "INSERT INTO your_table (image_id, data) VALUES (%s, %s)"
    session.execute(cql, (image_id, image_data))

def get_image_data(session, image_id):
    cql = "SELECT data FROM your_table WHERE image_id = %s"
    row = session.execute(cql, (image_id,)).one()
    if row:
        return row.data
    else:
        return None

# More CRUD operations as needed...