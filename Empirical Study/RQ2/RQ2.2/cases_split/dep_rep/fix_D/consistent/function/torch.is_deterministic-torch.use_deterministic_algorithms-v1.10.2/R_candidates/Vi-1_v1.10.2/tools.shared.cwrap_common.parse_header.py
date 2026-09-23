def parse_header(path: str) -> List[Function]:
    with open(path, 'r') as f:
        lines: Iterable[Any] = f.read().split('\n')

    # Remove empty lines and prebackend directives
    lines = filter(lambda l: l and not l.startswith('#'), lines)
    # Remove line comments
    lines = (l.partition('//') for l in lines)
    # Select line and comment part
    lines = ((l[0].strip(), l[2].strip()) for l in lines)
    # Remove trailing special signs
    lines = ((l[0].rstrip(');').rstrip(','), l[1]) for l in lines)
    # Split arguments
    lines = ((l[0].split(','), l[1]) for l in lines)
    # Flatten lines
    new_lines = []
    for l, c in lines:
        for split in l:
            new_lines.append((split, c))
    lines = new_lines
    del new_lines
    # Remove unnecessary whitespace
    lines = ((l[0].strip(), l[1]) for l in lines)
    # Remove empty lines
    lines = filter(lambda l: l[0], lines)
    generic_functions = []
    for l, c in lines:
        if l.startswith('TH_API void THNN_'):
            fn_name = l[len('TH_API void THNN_'):]
            if fn_name[0] == '(' and fn_name[-2] == ')':
                fn_name = fn_name[1:-2]
            else:
                fn_name = fn_name[:-1]
            generic_functions.append(Function(fn_name))
        elif l.startswith('TORCH_CUDA_CPP_API void THNN_'):
            fn_name = l[len('TORCH_CUDA_CPP_API void THNN_'):]
            if fn_name[0] == '(' and fn_name[-2] == ')':
                fn_name = fn_name[1:-2]
            else:
                fn_name = fn_name[:-1]
            generic_functions.append(Function(fn_name))
        elif l.startswith('TORCH_CUDA_CU_API void THNN_'):
            fn_name = l[len('TORCH_CUDA_CU_API void THNN_'):]
            if fn_name[0] == '(' and fn_name[-2] == ')':
                fn_name = fn_name[1:-2]
            else:
                fn_name = fn_name[:-1]
            generic_functions.append(Function(fn_name))
        elif l:
            t, name = l.split()
            if '*' in name:
                t = t + '*'
                name = name[1:]
            generic_functions[-1].add_argument(
                Argument(t, name, '[OPTIONAL]' in c))
    return generic_functions
