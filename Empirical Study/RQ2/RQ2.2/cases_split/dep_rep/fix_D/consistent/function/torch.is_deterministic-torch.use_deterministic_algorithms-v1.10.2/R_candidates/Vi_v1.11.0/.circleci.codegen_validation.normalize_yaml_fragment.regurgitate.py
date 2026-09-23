def regurgitate(depth, use_pyyaml_formatter=False):
    data = yaml.safe_load(sys.stdin)

    if use_pyyaml_formatter:
        output = yaml.dump(data, sort_keys=True)
        sys.stdout.write(output)
    else:
        miniyaml.render(sys.stdout, data, depth)
