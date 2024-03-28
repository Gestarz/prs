import hazelcast

client = hazelcast.HazelcastClient(cluster_name="lab2")
queue = client.get_queue("my-queue").blocking()

while True:
    consumed_item = queue.take()
    print(consumed_item)

