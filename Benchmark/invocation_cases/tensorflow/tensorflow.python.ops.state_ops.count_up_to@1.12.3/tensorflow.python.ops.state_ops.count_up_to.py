import tensorflow as tf
import inspect

if tf.__version__.startswith("1."):
    tf1 = tf
else:
    tf1 = tf.compat.v1
    tf1.disable_eager_execution() 

def main():
    # Create a variable with an initial value
    var = tf.Variable(0, dtype=tf.int32)
    
    # Initialize the variable
    init_op = tf1.global_variables_initializer()
    
    # Use count_up_to
    with tf1.Session() as sess:
        sess.run(init_op)
        result = tf.count_up_to(var, limit=5)
        print("count_up_to result:", sess.run(result))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.count_up_to))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()