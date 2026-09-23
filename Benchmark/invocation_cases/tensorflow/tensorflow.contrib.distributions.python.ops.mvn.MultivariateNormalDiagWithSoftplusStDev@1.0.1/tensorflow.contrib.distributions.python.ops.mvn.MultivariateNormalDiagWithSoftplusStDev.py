import tensorflow as tf
import inspect
from tensorflow.contrib.distributions.python.ops.mvn import MultivariateNormalDiagWithSoftplusStDev

def main():
    loc = tf.constant([0.0, 0.0])
    scale_diag = tf.constant([1.0, 1.0])

    mvn = MultivariateNormalDiagWithSoftplusStDev(loc, scale_diag)
    sample = mvn.sample()

    with tf.Session() as sess:
        result = sess.run(sample)
        print("Sample result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(MultivariateNormalDiagWithSoftplusStDev))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
