def main(argv):
    parser = argparse.ArgumentParser(description='Generate glsl.cpp and glsl.h containing glsl sources')
    parser.add_argument(
        '-i',
        '--glsl-path',
        help='path to directory with glsl to process',
        required=True,
        default='.')
    parser.add_argument(
        '-o',
        '--output-path',
        help='path to directory to generate glsl.h glsl.cpp (cpp namespace at::native::vulkan)',
        required=True)
    parser.add_argument(
        '-t',
        '--tmp-dir-path',
        required=True,
        help='/tmp')
    parser.add_argument(
        "--env",
        metavar="KEY=VALUE",
        nargs='*',
        help="Set a number of key-value pairs")
    options = parser.parse_args()
    if not os.path.exists(options.tmp_dir_path):
        os.makedirs(options.tmp_dir_path)
    env = DEFAULT_ENV
    for key, value in parse_arg_env(options.env).items():
        env[key] = value

    if not os.path.exists(options.output_path):
        os.makedirs(options.output_path)

    glsls = findAllGlsls(options.glsl_path)
    genCppH(
        options.output_path + "/" + H_NAME, options.output_path + "/" + CPP_NAME,
        glsls,
        tmpDirPath=options.tmp_dir_path,
        env=env)
