import hazelcast
import time


try:
    client = hazelcast.HazelcastClient(cluster_name="lab2")
    hz_topic = client.get_topic("my-topic").blocking()

    for i in range(1, 101):
        hz_topic.publish(f"Msg {i}")
        print(f"Published: {i}")
        time.sleep(1)

except Exception as e:
    print(f"An error occurred: {e}")
