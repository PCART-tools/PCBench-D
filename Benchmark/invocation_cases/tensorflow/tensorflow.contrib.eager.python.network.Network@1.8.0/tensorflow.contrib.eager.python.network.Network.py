import tensorflow as tf
import inspect

if tf.__version__.startswith("1."):
    tf1 = tf
else:
    tf1 = tf.compat.v1
    tf1.disable_eager_execution() 

def main():
    tf1.enable_eager_execution()

    class SimpleNetwork(tf.contrib.eager.Network):
        def __init__(self):
            super(SimpleNetwork, self).__init__()
            self.layer = tf.layers.Dense(10)

        def call(self, inputs):
            return self.layer(inputs)

    network = SimpleNetwork()
    inputs = tf.constant([[1.0, 2.0, 3.0]])
    result = network(inputs)
    print("Network result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.contrib.eager.Network))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()