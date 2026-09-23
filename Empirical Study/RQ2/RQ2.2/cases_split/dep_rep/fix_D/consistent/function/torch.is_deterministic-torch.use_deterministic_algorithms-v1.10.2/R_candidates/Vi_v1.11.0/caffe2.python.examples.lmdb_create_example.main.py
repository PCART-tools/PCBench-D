def main():
    parser = argparse.ArgumentParser(
        description="Example LMDB creation"
    )
    parser.add_argument("--output_file", type=str, default=None,
                        help="Path to write the database to",
                        required=True)

    args = parser.parse_args()
    checksum = create_db(args.output_file)

    # For testing reading:
    read_db_with_caffe2(args.output_file, checksum)
