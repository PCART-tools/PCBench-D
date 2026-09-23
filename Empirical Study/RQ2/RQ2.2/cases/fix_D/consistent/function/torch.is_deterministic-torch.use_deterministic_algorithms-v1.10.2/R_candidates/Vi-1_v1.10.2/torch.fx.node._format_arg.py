def _format_arg(arg) -> str:
    if isinstance(arg, list):
        items = ', '.join(_format_arg(a) for a in arg)
        return f'[{items}]'
    elif isinstance(arg, tuple):
        items = ', '.join(_format_arg(a) for a in arg)
        maybe_comma = ',' if len(arg) == 1 else ''
        return f'({items}{maybe_comma})'
    elif isinstance(arg, dict):
        items_str = ', '.join(f'{k}: {_format_arg(v)}' for k, v in arg.items())
        return f'{{{items_str}}}'

    if isinstance(arg, Node):
        return '%' + str(arg)
    else:
        return str(arg)
