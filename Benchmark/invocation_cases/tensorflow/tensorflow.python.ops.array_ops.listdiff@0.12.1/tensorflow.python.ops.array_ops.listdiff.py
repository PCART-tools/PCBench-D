import tensorflow as tf
from tensorflow.python.ops import array_ops
import inspect

if not tf.__version__.startswith("2."):
    tf1 = tf
else:
    tf1 = tf.compat.v1
    tf1.disable_eager_execution() 

def main():
    x = tf.constant([1, 2, 3, 4, 5])
    y = tf.constant([3, 4])
    result = array_ops.listdiff(x, y)

    with tf1.Session() as sess:
        out = sess.run(result[0])  # listdiff returns a tuple with the diff and idx
        print("listdiff result:", out)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(array_ops.listdiff))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()