def get_param(module, attr):
    """Get the parameter given a module and attribute.

    Sometimes the weights/bias attribute gives you the raw tensor, but sometimes
    gives a function that will give you the raw tensor, this function takes care of that logic
    """
    param = getattr(module, attr, None)
    if callable(param):
        return param()
    else:
        return param
