import tensorflow as tf
import inspect
from tensorflow.python.distribute.parameter_server_strategy import ParameterServerStrategy

def main():
    cluster_spec = tf.train.ClusterSpec({
        "worker": ["localhost:12345"],
        "ps": ["localhost:23456"]
    })

    cluster_resolver = tf.distribute.cluster_resolver.SimpleClusterResolver(
        cluster_spec=cluster_spec,
        task_type="worker",
        task_id=0
    )

    strategy = ParameterServerStrategy(cluster_resolver)
    print("ParameterServerStrategy instance created:", strategy)

    print("----- getsource_output -----")
    try:
        print(inspect.getsource(ParameterServerStrategy))
    except Exception as e:
        print("inspect failed:", type(e).__name__, str(e))

if __name__ == "__main__":
    main()
