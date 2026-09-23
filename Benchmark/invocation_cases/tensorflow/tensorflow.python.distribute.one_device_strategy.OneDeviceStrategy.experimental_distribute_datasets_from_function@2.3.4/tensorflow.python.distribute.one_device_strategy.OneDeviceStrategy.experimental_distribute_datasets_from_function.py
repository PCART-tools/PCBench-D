import tensorflow as tf
import inspect

def dataset_fn(input_context):
    batch_size = input_context.get_per_replica_batch_size(64)
    return tf.data.Dataset.from_tensor_slices([1, 2, 3, 4]).batch(batch_size)

def main():
    strategy = tf.distribute.OneDeviceStrategy(device="/cpu:0")
    distributed_dataset = strategy.experimental_distribute_datasets_from_function(dataset_fn)
    
    for batch in distributed_dataset:
        print("Batch:", batch.numpy())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(strategy.experimental_distribute_datasets_from_function))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()