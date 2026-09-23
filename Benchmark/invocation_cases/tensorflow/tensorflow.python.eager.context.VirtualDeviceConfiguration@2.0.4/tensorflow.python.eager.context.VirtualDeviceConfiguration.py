import tensorflow as tf
import inspect

def main():
    # Create a virtual device configuration
    virtual_device_config = tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)
    print("VirtualDeviceConfiguration:", virtual_device_config)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.config.experimental.VirtualDeviceConfiguration))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()