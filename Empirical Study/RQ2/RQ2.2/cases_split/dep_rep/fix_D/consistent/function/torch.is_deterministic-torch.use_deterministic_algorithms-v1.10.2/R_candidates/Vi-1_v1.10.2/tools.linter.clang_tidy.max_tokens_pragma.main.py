def main() -> None:
    options = parse_args()

    ignored = set(options.ignore)
    files = [filename for filename in options.files if filename not in ignored]
    if options.strip:
        strip_max_tokens_pragma_from_files(files)
    else:
        add_max_tokens_pragma_to_files(files, options.num_max_tokens)
