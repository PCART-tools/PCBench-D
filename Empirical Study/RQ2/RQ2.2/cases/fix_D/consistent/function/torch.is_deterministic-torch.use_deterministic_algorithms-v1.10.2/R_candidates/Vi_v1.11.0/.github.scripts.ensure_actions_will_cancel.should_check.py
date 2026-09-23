def should_check(filename: Path) -> bool:
    with open(filename, "r") as f:
        content = f.read()

    data = yaml.safe_load(content)
    on = data.get("on", data.get(True, {}))
    return "pull_request" in on
