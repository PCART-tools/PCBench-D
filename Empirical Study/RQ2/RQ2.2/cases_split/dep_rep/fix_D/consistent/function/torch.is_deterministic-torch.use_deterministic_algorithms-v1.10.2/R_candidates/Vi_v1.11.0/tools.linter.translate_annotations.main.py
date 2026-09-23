def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('--regex')
    parser.add_argument('--commit')
    args = parser.parse_args()
    with open(args.file, 'r') as f:
        lines = f.readlines()
    print(json.dumps(translate_all(
        lines=lines,
        regex=args.regex,
        commit=args.commit
    )))
