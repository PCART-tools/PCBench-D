def read_resource_file(resource_file: str) -> str:
    with open(os.path.join(os.path.dirname(__file__), resource_file), "r") as fp:
        return "".join(fp.readlines())
