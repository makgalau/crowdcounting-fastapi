crowd_count_table = "crowd_count"


def get(client):
    data = client.table(crowd_count_table).select("*").order("created_at").execute()
    return data.data


def insert(client, **args):
    _, _ = client.table(crowd_count_table).insert([args]).execute()
    return


def delete(client, id):
    query = f"DELETE FROM {crowd_count_table} WHERE id = {id}"
    response = client.query(query)
    return