import hazelcast

client = hazelcast.HazelcastClient(cluster_name="lab2")
hz_map = client.get_map("my-map").blocking()

try:
    for i in range(1000):
        hz_map.put(i, f"value{i}")
except Exception as e:
    print(f"An error occurred: {e}")
