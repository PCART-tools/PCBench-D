def main() -> None:
    parser = argparse.ArgumentParser(description='Generate Lazy Tensor backend files')
    parser.add_argument(
        '-s',
        '--source_yaml',
        help='path to source yaml file containing operator external definitions')
    parser.add_argument(
        '-o', '--output_dir', help='output directory')
    parser.add_argument(
        '--dry_run', type=bool, default=False, help='output directory')
    parser.add_argument(
        '--impl_path', type=str, default=None, help='path to the source C++ file containing kernel definitions')
    parser.add_argument(
        '--gen_ts_lowerings', action="store_true", help='Generate TorchScript lowerings in addition to Lazy IR and NativeFunctions')
    parser.add_argument(
        '--node_base', type=str, default="Node", help='Name of backend specific custom Lazy IR Node base class')
    parser.add_argument(
        '--node_base_hdr', type=str, default=None, help='Path to header file defining custom Lazy IR Node base class')
    parser.add_argument(
        '--tensor_class', type=str, default="LazyTensor", help='Name of backend specific custom Lazy Tensor class')
    parser.add_argument(
        '--tensor_class_hdr', type=str, default="lazy_tensor_core/csrc/tensor.h",
        help='Path to header file defining custom Lazy Tensor class')
    options = parser.parse_args()

    run(options.source_yaml, options.output_dir, options.dry_run, options.impl_path,
        options.gen_ts_lowerings, options.node_base, options.node_base_hdr,
        options.tensor_class, options.tensor_class_hdr)
