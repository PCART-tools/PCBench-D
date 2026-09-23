def parse_arguments(args: List[Union[str, Arg]]) -> List[Arg]:
    new_args = []
    for arg in args:
        # Simple arg declaration of form "<type> <name>"
        if isinstance(arg, str):
            t, _, name = arg.partition(' ')
            new_args.append({'type': t, 'name': name})
        elif isinstance(arg, dict):
            if 'arg' in arg:
                arg['type'], _, arg['name'] = arg['arg'].partition(' ')
                del arg['arg']
            new_args.append(arg)
        else:
            raise AssertionError()
    return new_args
