@utils.debug
def main():
    parser = argparse.ArgumentParser(
        description="Caffe2: Char RNN Training"
    )
    parser.add_argument("--train_data", type=str, default=None,
                        help="Path to training data in a text file format",
                        required=True)
    parser.add_argument("--seq_length", type=int, default=25,
                        help="One training example sequence length")
    parser.add_argument("--batch_size", type=int, default=1,
                        help="Training batch size")
    parser.add_argument("--iters_to_report", type=int, default=500,
                        help="How often to report loss and generate text")
    parser.add_argument("--hidden_size", type=int, default=100,
                        help="Dimension of the hidden representation")
    parser.add_argument("--gpu", action="store_true",
                        help="If set, training is going to use GPU 0")

    args = parser.parse_args()

    device = core.DeviceOption(
        workspace.GpuDeviceType if args.gpu else caffe2_pb2.CPU, 0)
    with core.DeviceScope(device):
        model = CharRNN(args)
        model.CreateModel()
        model.TrainModel()
