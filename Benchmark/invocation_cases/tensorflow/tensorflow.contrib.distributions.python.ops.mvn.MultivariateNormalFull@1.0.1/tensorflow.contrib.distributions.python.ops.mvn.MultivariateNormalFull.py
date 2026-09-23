import tensorflow as tf
import inspect

def main():
    # Simulate input data
    mean = [0.0, 0.0]
    covariance_matrix = [[1.0, 0.0], [0.0, 1.0]]
    
    # Create a MultivariateNormalFull object
    mvn = tf.contrib.distributions.MultivariateNormalFull(mean, covariance_matrix)
    
    # Sample from the distribution
    sample = mvn.sample()
    with tf.Session() as sess:
        result = sess.run(sample)
        print("MultivariateNormalFull sample:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.contrib.distributions.MultivariateNormalFull))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()