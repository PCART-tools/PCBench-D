def load_data(args):
    r"""
    A function that creates an instance of the data class.
    Args:
        args (parser): launcher configurations
    """
    data_config_file = args.data_config_path
    data_config = get_json_config(data_config_file, args.data)
    data_class = data_map[data_config["data_class"]]
    return data_class(**data_config["configurations"])
