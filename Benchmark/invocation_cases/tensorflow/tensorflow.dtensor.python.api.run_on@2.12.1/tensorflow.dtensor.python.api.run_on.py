import tensorflow as tf
import inspect
from tensorflow.experimental import dtensor
from tensorflow.dtensor.python.api import run_on


def main():
    mesh = dtensor.create_mesh([("CPU", 1)])
    layout = dtensor.Layout.replicated(mesh, rank=1)

    with run_on(mesh):
        x = dtensor.copy_to_mesh(tf.constant([1.0, 2.0, 3.0]), layout)
        result = x * 5
        print("run_on result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(run_on))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
