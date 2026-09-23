def load_model(args):
    r"""
    A function that creates an instance of the model class.
    Args:
        args (parser): launcher configurations
    """
    model_config_file = args.model_config_path
    model_config = get_json_config(model_config_file, args.model)
    model_class = model_map[model_config["model_class"]]
    return model_class(**model_config["configurations"])
