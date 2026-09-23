import tensorflow as tf
import inspect

def main():
    # Create dummy datasets
    dataset1 = tf.data.Dataset.from_tensor_slices([1, 2, 3])
    dataset2 = tf.data.Dataset.from_tensor_slices([4, 5, 6])
    
    # Use sample_from_datasets
    result = tf.data.experimental.sample_from_datasets([dataset1, dataset2])
    for element in result.take(6):
        print(element.numpy())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.data.experimental.sample_from_datasets))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()