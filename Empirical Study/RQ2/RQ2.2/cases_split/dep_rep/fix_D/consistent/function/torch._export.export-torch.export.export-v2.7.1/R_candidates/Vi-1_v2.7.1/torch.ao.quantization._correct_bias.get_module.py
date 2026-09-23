def get_module(model, name):
    """Given name of submodule, this function grabs the submodule from given model."""
    return dict(model.named_modules())[name]
