import tensorflow as tf
import inspect

def main():
    result = tf.config.experimental_list_devices()
    print("experimental_list_devices result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.config.experimental_list_devices))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
