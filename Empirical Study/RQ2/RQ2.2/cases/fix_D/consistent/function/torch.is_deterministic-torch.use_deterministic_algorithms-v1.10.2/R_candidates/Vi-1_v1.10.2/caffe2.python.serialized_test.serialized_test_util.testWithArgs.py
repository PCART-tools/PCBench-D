def testWithArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-G', '--generate-serialized', action='store_true', dest='generate',
        help='generate output files (default=false, compares to current files)')
    parser.add_argument(
        '-O', '--output', default=DATA_DIR,
        help='output directory (default: %(default)s)')
    parser.add_argument(
        '-D', '--disable-serialized_check', action='store_true', dest='disable',
        help='disable checking serialized tests')
    parser.add_argument(
        '-C', '--disable-gen-coverage', action='store_true',
        dest='disable_coverage',
        help='disable generating coverage markdown file')
    parser.add_argument('unittest_args', nargs='*')
    args = parser.parse_args()
    sys.argv[1:] = args.unittest_args
    _output_context.__setattr__('should_generate_output', args.generate)
    _output_context.__setattr__('output_dir', args.output)
    _output_context.__setattr__('disable_serialized_check', args.disable)
    _output_context.__setattr__('disable_gen_coverage', args.disable_coverage)

    import unittest
    unittest.main()
