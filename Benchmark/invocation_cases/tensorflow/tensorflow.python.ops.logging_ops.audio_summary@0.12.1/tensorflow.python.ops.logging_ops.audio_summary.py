import tensorflow as tf
import inspect

def main():
    with tf.Session() as sess:
        audio_tensor = tf.constant([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]], dtype=tf.float32)
        summary_op = tf.audio_summary('audio', audio_tensor, sample_rate=44100)
        summary = sess.run(summary_op)
        print("audio_summary result:", summary)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.audio_summary))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()