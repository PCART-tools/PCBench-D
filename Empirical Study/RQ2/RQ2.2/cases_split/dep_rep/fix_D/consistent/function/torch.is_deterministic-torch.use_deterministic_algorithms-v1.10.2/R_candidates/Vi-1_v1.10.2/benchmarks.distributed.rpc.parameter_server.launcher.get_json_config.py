def get_json_config(file_name, id):
    r"""
    A function that loads a json configuration from a file.
    Args:
        file_name (str): name of configuration file to load
        id (str): configuration that will be loaded
    """
    with open(os.path.join(Path(__file__).parent, file_name), "r") as f:
        json_config = json.load(f)[id]
    return json_config
