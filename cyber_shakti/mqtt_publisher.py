import paho.mqtt.client as mqtt

# MQTT Broker Configuration
broker = "13.201.16.233"  # Replace with the IP or domain of your MQTT broker
port = 1883           # Default port for MQTT
topic = "sensor/temperature"  # The topic to publish to
message = "147C"  # The message to publish

def publish_message():
    try:
        # Create an MQTT client instance
        client = mqtt.Client()

        # Connect to the MQTT broker
        client.connect(broker, port, 60)

        # Publish the message to the topic
        client.publish(topic, message)
        print(f"Message '{message}' published to topic '{topic}'")

        # Disconnect from the broker
        client.disconnect()

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
if __name__ == "__main__":
    message = 247.0
    
    
    publish_message()
    