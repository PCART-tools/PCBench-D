def required_attribute_names(o):
    return sorted([a['name'] for a in o['arguments'] if not value_has_tensors(a) and 'default' not in a])
