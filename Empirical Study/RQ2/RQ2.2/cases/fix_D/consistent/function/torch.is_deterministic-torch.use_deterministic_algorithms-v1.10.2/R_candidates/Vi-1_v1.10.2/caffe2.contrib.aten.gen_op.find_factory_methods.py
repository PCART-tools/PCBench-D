def find_factory_methods(decls):
    factory_methods = {}
    for o in decls:
        if any(arg['dynamic_type'] == 'at::TensorOptions' for arg in o['arguments']):
            factory_methods[o['name']] = 0
    return factory_methods
