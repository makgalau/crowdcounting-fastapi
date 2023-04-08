crowd_count_table = "crowd_count"


def get(client):
    data = client.table(crowd_count_table).select("*").execute()
    return data.data


def insert(client, **args):
    _, _ = client.table(crowd_count_table).insert([args]).execute()
    return
