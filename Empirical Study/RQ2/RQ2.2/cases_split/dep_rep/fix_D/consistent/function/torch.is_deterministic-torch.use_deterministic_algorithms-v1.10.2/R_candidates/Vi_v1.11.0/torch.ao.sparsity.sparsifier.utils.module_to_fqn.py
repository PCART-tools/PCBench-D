def module_to_fqn(model, layer, prefix=''):
    for name, child in model.named_children():
        new_name = prefix + '.' + name
        if child is layer:
            return new_name
        child_path = module_to_fqn(child, layer, prefix=new_name)
        if child_path is not None:
            return child_path
    return None
