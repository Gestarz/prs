import hazelcast


client = hazelcast.HazelcastClient(cluster_name="lab2")

queue = client.get_queue("my-queue").blocking()
for i in range(100):
    queue.put(i)
    print(f"Producing {i}")
