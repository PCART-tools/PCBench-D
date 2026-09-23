def GetArgumentParser():
    parser = argparse.ArgumentParser(description="Caffe2 optimization")
    parser.add_argument("--init_net",
                        type=argparse.FileType('rb'),
                        help="init net")
    parser.add_argument("--pred_net",
                        type=argparse.FileType('rb'),
                        help="predict net")
    parser.add_argument("--verify_input",
                        type=argparse.FileType('r'),
                        help="input dims for verification")
    parser.add_argument("--fuse_bn", default=False, action='store_true')
    parser.add_argument("--fuse_mul_add", default=False, action='store_true')
    parser.add_argument("--fuse_conv_relu", default=False, action='store_true')
    return parser
