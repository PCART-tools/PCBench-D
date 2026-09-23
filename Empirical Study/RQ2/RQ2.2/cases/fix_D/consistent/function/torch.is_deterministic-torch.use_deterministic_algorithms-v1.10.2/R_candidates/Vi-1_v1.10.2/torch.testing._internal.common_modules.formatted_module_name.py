def formatted_module_name(module_cls):
    """ Returns the common name of the module class formatted for use in test names. """
    return MODULE_CLASS_NAMES[module_cls].replace('.', '_')
