def pytest_addoption(parser):
    parser.addoption(
        '-G',
        '--generate-serialized',
        action='store_true',
        dest='generate',
        help='generate output files (default=false, compares to current files)',
    )
    parser.addoption(
        '-O',
        '--output',
        default=serial.DATA_DIR,
        dest='output',
        help='output directory (default: %(default)s)'
    )
    parser.addoption(
        '-D',
        '--disable-serialized-check',
        action='store_true',
        dest='disable',
        help='disable checking serialized tests'
    )
    parser.addoption(
        '-C',
        '--disable-gen-coverage',
        action='store_true',
        dest='disable_coverage',
        help='disable generating coverage markdown file'
    )
