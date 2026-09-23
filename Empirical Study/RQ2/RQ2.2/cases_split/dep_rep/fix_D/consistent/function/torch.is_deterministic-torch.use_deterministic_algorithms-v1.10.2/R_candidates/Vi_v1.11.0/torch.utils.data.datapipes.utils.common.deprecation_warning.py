def deprecation_warning(name, new_name: str = ""):
    new_name_statement = ""
    if new_name:
        new_name_statement = f" Please use {new_name} instead."
    warnings.warn(f"{name} and its functional API are deprecated and will be removed from the package `torch`." +
                  new_name_statement, DeprecationWarning)
