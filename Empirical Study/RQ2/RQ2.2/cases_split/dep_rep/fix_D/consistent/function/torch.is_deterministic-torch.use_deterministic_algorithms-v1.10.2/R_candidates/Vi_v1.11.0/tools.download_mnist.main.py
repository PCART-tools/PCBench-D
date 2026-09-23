def main() -> None:
    parser = argparse.ArgumentParser(
        description='Download the MNIST dataset from the internet')
    parser.add_argument(
        '-d', '--destination', default='.', help='Destination directory')
    parser.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help="Don't report about progress")
    options = parser.parse_args()

    if not os.path.exists(options.destination):
        os.makedirs(options.destination)

    try:
        for resource in RESOURCES:
            path = os.path.join(options.destination, resource)
            download(path, resource, options.quiet)
            unzip(path, options.quiet)
    except KeyboardInterrupt:
        print('Interrupted')
