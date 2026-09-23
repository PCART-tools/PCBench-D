import tensorflow as tf
import inspect
from tensorflow.python.ops import logging_ops

if not tf.__version__.startswith("2."):
    tf1 = tf
else:
    tf1 = tf.compat.v1
    tf1.disable_eager_execution() 

def main():
    # Simulate input data
    images = tf1.random_uniform([2, 8, 8, 3], maxval=255, dtype=tf.int32)
    images = tf.cast(images, tf.uint8)
    
    # Call the target API
    summary_op = logging_ops.image_summary("images", images)
    with tf1.Session() as sess:
        summary = sess.run(summary_op)
        print("image_summary result:", summary)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(logging_ops.image_summary))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()