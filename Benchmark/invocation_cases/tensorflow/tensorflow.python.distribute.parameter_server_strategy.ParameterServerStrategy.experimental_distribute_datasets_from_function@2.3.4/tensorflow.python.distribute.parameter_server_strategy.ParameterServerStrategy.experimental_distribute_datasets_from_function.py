import tensorflow as tf
import inspect
from tensorflow.python.distribute.parameter_server_strategy import ParameterServerStrategy

tf.compat.v1.disable_eager_execution()

def dataset_fn(input_context):
    global_batch_size = 64
    batch_size = input_context.get_per_replica_batch_size(global_batch_size)
    d = tf.data.Dataset.from_tensors(([1.0], [2.0])).repeat().batch(batch_size)
    return d.shard(input_context.num_input_pipelines, input_context.input_pipeline_id)

def model_fn(features, labels, mode):
    logits = tf.compat.v1.layers.dense(features, units=1)
    loss = tf.compat.v1.losses.mean_squared_error(labels=labels, predictions=logits)

    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.compat.v1.train.GradientDescentOptimizer(0.01)
        train_op = optimizer.minimize(loss, global_step=tf.compat.v1.train.get_or_create_global_step())
        return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op)
    else:
        return tf.estimator.EstimatorSpec(mode, loss=loss)

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

    strategy.experimental_distribute_datasets_from_function(dataset_fn)
    print("Called experimental_distribute_datasets_from_function")

    print("----- getsource_output -----")
    try:
        print(inspect.getsource(ParameterServerStrategy.experimental_distribute_datasets_from_function))
    except Exception as e:
        print("inspect failed:", type(e).__name__, str(e))

    config = tf.estimator.RunConfig(train_distribute=strategy)
    estimator = tf.estimator.Estimator(model_fn=model_fn, config=config)

if __name__ == "__main__":
    main()
