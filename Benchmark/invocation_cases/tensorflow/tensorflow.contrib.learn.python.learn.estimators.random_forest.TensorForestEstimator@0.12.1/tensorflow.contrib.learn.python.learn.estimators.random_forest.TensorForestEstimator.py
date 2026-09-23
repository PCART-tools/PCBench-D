import tensorflow as tf
import inspect
import numpy as np

def main():
    # Simulate input data
    features = np.array([[1.0], [2.0], [3.0]], dtype=np.float32)
    labels = np.array([[0], [1], [0]], dtype=np.int32)

    # Create a TensorForestEstimator
    estimator = tf.contrib.learn.TensorForestEstimator(
        params=tf.contrib.tensor_forest.python.tensor_forest.ForestHParams(
            num_classes=2, num_features=1
        )
    )

    # Fit the estimator using input_fn
    def input_fn():
        return tf.constant(features), tf.constant(labels)

    estimator.fit(input_fn=input_fn, steps=10)

    # Output the result
    print("Estimator trained.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.contrib.learn.TensorForestEstimator))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()