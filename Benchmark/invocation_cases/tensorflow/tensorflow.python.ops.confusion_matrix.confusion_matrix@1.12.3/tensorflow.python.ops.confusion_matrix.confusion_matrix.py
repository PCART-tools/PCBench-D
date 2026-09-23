import tensorflow as tf
import inspect

def main():
    labels = [0, 1, 2, 2, 1]
    predictions = [0, 2, 1, 2, 0]
    result = tf.confusion_matrix(labels, predictions)
    with tf.Session() as sess:
        print("Confusion Matrix:\n", sess.run(result))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.confusion_matrix))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()