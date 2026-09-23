def get_layer_scope(scope, layer_type, i):
    prefix = (scope + '/' if scope else '') + layer_type
    return '{}/layer{}'.format(prefix, i)
