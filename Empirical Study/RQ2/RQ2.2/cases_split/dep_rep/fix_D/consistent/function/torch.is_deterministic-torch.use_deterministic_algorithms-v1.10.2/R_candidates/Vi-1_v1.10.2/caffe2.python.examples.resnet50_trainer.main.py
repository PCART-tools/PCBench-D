def main():
    # TODO: use argv
    parser = argparse.ArgumentParser(
        description="Caffe2: ImageNet Trainer"
    )
    parser.add_argument("--train_data", type=str, default=None, required=True,
                        help="Path to training data (or 'null' to simulate)")
    parser.add_argument("--num_layers", type=int, default=50,
                        help="The number of layers in ResNe(X)t model")
    parser.add_argument("--resnext_num_groups", type=int, default=1,
                        help="The cardinality of resnext")
    parser.add_argument("--resnext_width_per_group", type=int, default=64,
                        help="The cardinality of resnext")
    parser.add_argument("--test_data", type=str, default=None,
                        help="Path to test data")
    parser.add_argument("--image_mean_per_channel", type=float, nargs='+',
                        help="The per channel mean for the images")
    parser.add_argument("--image_std_per_channel", type=float, nargs='+',
                        help="The per channel standard deviation for the images")
    parser.add_argument("--test_epoch_size", type=int, default=50000,
                        help="Number of test images")
    parser.add_argument("--db_type", type=str, default="lmdb",
                        help="Database type (such as lmdb or leveldb)")
    parser.add_argument("--gpus", type=str,
                        help="Comma separated list of GPU devices to use")
    parser.add_argument("--num_gpus", type=int, default=1,
                        help="Number of GPU devices (instead of --gpus)")
    parser.add_argument("--num_channels", type=int, default=3,
                        help="Number of color channels")
    parser.add_argument("--image_size", type=int, default=224,
                        help="Input image size (to crop to)")
    parser.add_argument("--num_labels", type=int, default=1000,
                        help="Number of labels")
    parser.add_argument("--batch_size", type=int, default=32,
                        help="Batch size, total over all GPUs")
    parser.add_argument("--epoch_size", type=int, default=1500000,
                        help="Number of images/epoch, total over all machines")
    parser.add_argument("--num_epochs", type=int, default=1000,
                        help="Num epochs.")
    parser.add_argument("--base_learning_rate", type=float, default=0.1,
                        help="Initial learning rate.")
    parser.add_argument("--weight_decay", type=float, default=1e-4,
                        help="Weight decay (L2 regularization)")
    parser.add_argument("--cudnn_workspace_limit_mb", type=int, default=64,
                        help="CuDNN workspace limit in MBs")
    parser.add_argument("--num_shards", type=int, default=1,
                        help="Number of machines in distributed run")
    parser.add_argument("--shard_id", type=int, default=0,
                        help="Shard id.")
    parser.add_argument("--run_id", type=str,
                        help="Unique run identifier (e.g. uuid)")
    parser.add_argument("--redis_host", type=str,
                        help="Host of Redis server (for rendezvous)")
    parser.add_argument("--redis_port", type=int, default=6379,
                        help="Port of Redis server (for rendezvous)")
    parser.add_argument("--file_store_path", type=str, default="/tmp",
                        help="Path to directory to use for rendezvous")
    parser.add_argument("--save_model_name", type=str, default="resnext_model",
                        help="Save the trained model to a given name")
    parser.add_argument("--load_model_path", type=str, default=None,
                        help="Load previously saved model to continue training")
    parser.add_argument("--use_cpu", action="store_true",
                        help="Use CPU instead of GPU")
    parser.add_argument("--use_nccl", action="store_true",
                        help="Use nccl for inter-GPU collectives")
    parser.add_argument("--use_ideep", type=bool, default=False,
                        help="Use ideep")
    parser.add_argument('--dtype', default='float',
                        choices=['float', 'float16'],
                        help='Data type used for training')
    parser.add_argument('--float16_compute', action='store_true',
                        help="Use float 16 compute, if available")
    parser.add_argument('--enable_tensor_core', action='store_true',
                        help='Enable Tensor Core math for Conv and FC ops')
    parser.add_argument("--distributed_transport", type=str, default="tcp",
                        help="Transport to use for distributed run [tcp|ibverbs]")
    parser.add_argument("--distributed_interfaces", type=str, default="",
                        help="Network interfaces to use for distributed run")

    parser.add_argument("--first_iter_timeout", type=int, default=1200,
                        help="Timeout (secs) of the first iteration "
                        "(default: %(default)s)")
    parser.add_argument("--timeout", type=int, default=60,
                        help="Timeout (secs) of each (except the first) iteration "
                        "(default: %(default)s)")
    parser.add_argument("--model",
                        default="resnext", const="resnext", nargs="?",
                        choices=["shufflenet", "resnext"],
                        help="List of models which can be run")
    args = parser.parse_args()

    Train(args)
