import tensorflow as tf
import inspect

from tensorflow.contrib.labeled_tensor.python.ops import core
from tensorflow.contrib.labeled_tensor.python.ops import ops as labeled_ops

def main():
    # Simulate input data
    tensor = tf.constant([[1, 2], [3, 4]])

    labeled = core.LabeledTensor(
        tensor, axes=['x', 'y']
    )
    unpacked_tensors = labeled_ops.unpack(labeled)
    print("unpacked_tensors:", unpacked_tensors)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(labeled_ops.unpack))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
