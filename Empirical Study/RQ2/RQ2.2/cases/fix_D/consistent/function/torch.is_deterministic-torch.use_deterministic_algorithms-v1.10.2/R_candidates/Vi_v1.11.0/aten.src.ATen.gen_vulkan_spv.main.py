def main(argv):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '-i',
        '--glsl-path',
        help='',
        default='.')
    parser.add_argument(
        '-c',
        '--glslc-path',
        required=True,
        help='')
    parser.add_argument(
        '-t',
        '--tmp-dir-path',
        required=True,
        help='/tmp')
    parser.add_argument(
        '-o',
        '--output-path',
        required=True,
        help='')
    parser.add_argument(
        "--env",
        metavar="KEY=VALUE",
        nargs='*',
        help="Set a number of key-value pairs")
    options = parser.parse_args()
    env = DEFAULT_ENV
    for key, value in parse_arg_env(options.env).items():
        env[key] = value

    if not os.path.exists(options.output_path):
        os.makedirs(options.output_path)

    if not os.path.exists(options.tmp_dir_path):
        os.makedirs(options.tmp_dir_path)

    genCppH(
        hFilePath=options.output_path + "/spv.h",
        cppFilePath=options.output_path + "/spv.cpp",
        srcDirPath=options.glsl_path,
        glslcPath=options.glslc_path,
        tmpDirPath=options.tmp_dir_path,
        env=env)
