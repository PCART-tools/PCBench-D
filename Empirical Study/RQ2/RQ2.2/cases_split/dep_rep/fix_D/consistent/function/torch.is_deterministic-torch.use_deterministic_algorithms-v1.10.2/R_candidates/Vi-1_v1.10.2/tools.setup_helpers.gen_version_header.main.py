def main(args: argparse.Namespace) -> None:
    with open(args.version_path) as f:
        version = f.read().strip()
    (major, minor, patch) = parse_version(version)

    replacements = {
        "@TORCH_VERSION_MAJOR@": str(major),
        "@TORCH_VERSION_MINOR@": str(minor),
        "@TORCH_VERSION_PATCH@": str(patch),
    }

    # Create the output dir if it doesn't exist.
    os.makedirs(os.path.dirname(args.output_path), exist_ok=True)

    with open(args.template_path) as input:
        with open(args.output_path, "w") as output:
            for line in input.readlines():
                output.write(apply_replacements(replacements, line))
