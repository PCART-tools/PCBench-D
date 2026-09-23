import tensorflow as tf
from tensorflow.contrib.labeled_tensor import pack
from tensorflow.contrib.labeled_tensor.python.ops import core
import inspect

def main():
    t1 = tf.constant([1, 2])
    t2 = tf.constant([3, 4])


    lt1 = core.LabeledTensor(t1, axes=['x'])
    lt2 = core.LabeledTensor(t2, axes=['x'])

    result = pack(
        labeled_tensors=[lt1, lt2],
        new_axis='batch',      
        axis_position=0
    )

    print("pack result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pack))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()