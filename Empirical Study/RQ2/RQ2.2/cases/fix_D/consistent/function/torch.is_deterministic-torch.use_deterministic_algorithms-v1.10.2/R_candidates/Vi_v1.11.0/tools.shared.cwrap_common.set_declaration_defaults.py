def set_declaration_defaults(declaration: Declaration) -> None:
    if 'schema_string' not in declaration:
        # This happens for legacy TH bindings like
        # _thnn_conv_depthwise2d_backward
        declaration['schema_string'] = ''
    declaration.setdefault('arguments', [])
    declaration.setdefault('return', 'void')
    if 'cname' not in declaration:
        declaration['cname'] = declaration['name']
    if 'backends' not in declaration:
        declaration['backends'] = ['CPU', 'CUDA']
    assert 'api_name' not in declaration
    declaration['api_name'] = declaration['name']
    # NB: keep this in sync with gen_autograd.py
    if declaration.get('overload_name'):
        declaration['type_wrapper_name'] = "{}_{}".format(
            declaration['name'], declaration['overload_name'])
    else:
        declaration['type_wrapper_name'] = declaration['name']
    # TODO: Uggggh, parsing the schema string here, really???
    declaration['operator_name_with_overload'] = declaration['schema_string'].split('(')[0]
    if declaration['schema_string']:
        declaration['unqual_schema_string'] = declaration['schema_string'].split('::')[1]
        declaration['unqual_operator_name_with_overload'] = declaration['operator_name_with_overload'].split('::')[1]
    else:
        declaration['unqual_schema_string'] = ''
        declaration['unqual_operator_name_with_overload'] = ''
    # Simulate multiple dispatch, even if it's not necessary
    if 'options' not in declaration:
        declaration['options'] = [{
            'arguments': copy.deepcopy(declaration['arguments']),
            'schema_order_arguments': copy.deepcopy(declaration['schema_order_arguments']),
        }]
        del declaration['arguments']
        del declaration['schema_order_arguments']
    # Parse arguments (some of them can be strings)
    for option in declaration['options']:
        option['arguments'] = parse_arguments(option['arguments'])
        option['schema_order_arguments'] = parse_arguments(option['schema_order_arguments'])
    # Propagate defaults from declaration to options
    for option in declaration['options']:
        for k, v in declaration.items():
            # TODO(zach): why does cwrap not propagate 'name'? I need it
            # propagaged for ATen
            if k != 'options':
                option.setdefault(k, v)
