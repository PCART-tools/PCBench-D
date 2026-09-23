def run(args, submod):
    print(f"## Processing torch.{submod}")
    prev_filename = f"prev_data_{submod}.json"
    new_filename = f"new_data_{submod}.json"

    if args.prev_version:
        content = get_content(submod)
        with open(prev_filename, "w") as f:
            json.dump(content, f)
        print("Data saved for previous version.")
    elif args.new_version:
        content = get_content(submod)
        with open(new_filename, "w") as f:
            json.dump(content, f)
        print("Data saved for new version.")
    else:
        assert args.compare
        if not path.exists(prev_filename):
            raise RuntimeError("Previous version data not collected")

        if not path.exists(new_filename):
            raise RuntimeError("New version data not collected")

        with open(prev_filename, "r") as f:
            prev_content = set(json.load(f))

        with open(new_filename, "r") as f:
            new_content = set(json.load(f))

        if not args.show_all:
            prev_content = namespace_filter(prev_content)
            new_content = namespace_filter(new_content)

        if new_content == prev_content:
            print("Nothing changed.")
            print("")
        else:
            print("Things that were added:")
            print(new_content - prev_content)
            print("")

            print("Things that were removed:")
            print(prev_content - new_content)
            print("")
