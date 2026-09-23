import tensorflow as tf
from tensorflow.python.saved_model import loader_impl
import inspect
import os

if tf.__version__.startswith("1."):
    tf1 = tf
else:
    tf1 = tf.compat.v1
    tf1.disable_eager_execution() 

def main():
    export_path = os.path.join(os.getcwd(), "test_model")
    with tf1.Session() as load_sess:
        loader_impl.load(load_sess, [tf1.saved_model.tag_constants.SERVING], export_path)
        print("Model loaded successfully.")
    
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(loader_impl.load))
    except Exception as e:
        print(type(e).__name__)


if __name__ == "__main__":
    main()
