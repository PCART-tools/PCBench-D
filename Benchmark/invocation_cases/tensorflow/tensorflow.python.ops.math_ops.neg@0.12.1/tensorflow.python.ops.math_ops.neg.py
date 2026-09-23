import tensorflow as tf
import inspect

def main():
    # Create a TensorFlow constant
    x = tf.constant([1.0, -2.0, 3.0], dtype=tf.float32)
    
    # Call the neg function
    result = tf.neg(x)
    with tf.Session() as sess:
        output = sess.run(result)
        print("neg result:", output)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.neg))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()