import tensorflow as tf
import inspect
from tensorflow.python.eager import backprop
from tensorflow.python.framework.ops import enable_eager_execution

def main():
    enable_eager_execution()

    x = tf.constant([3.0])
    with backprop.GradientTape() as tape:
        tape.watch(x)
        y = tf.reduce_sum(x * x)  # Make y a scalar
    dy_dx = tape.gradient(y, x)

    print("Gradient:", dy_dx)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(backprop.GradientTape))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
