import hazelcast
from datetime import datetime


try:
    client = hazelcast.HazelcastClient(cluster_name="lab2")
    hz_topic = client.get_topic("my-topic").blocking()

    def message_listener(event):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print(f"Received: {event.message} at {current_time}")

    hz_topic.add_listener(message_listener)

    print("listening")
    input("press enter to stop\n")

except Exception as e:
    print(f"An error occurred: {e}")

