def emit_view_lambda(f: NativeFunction, unpacked_bindings: List[Binding]) -> str:
    """ Generate an additional lambda function to recover views in backward when as_strided is not supported.
    See Note [View + Inplace update for base tensor] and [View + Inplace update for view tensor] for more details."""
    input_base = 'input_base'
    replay_view_func = ''
    updated_unpacked_args: List[str] = []
    known_view_arg_simple_types: List[CType] = [
        BaseCType(longT),
        OptionalCType(BaseCType(longT)),
        BaseCType(boolT),
        BaseCType(intArrayRefT)]
    for unpacked_binding in unpacked_bindings:
        arg, arg_type = unpacked_binding.name, unpacked_binding.nctype.type
        if arg == 'self_':
            updated_unpacked_args.append(input_base)
            continue
        if arg_type not in known_view_arg_simple_types:
            known_types_str = ', '.join([str(t) for t in known_view_arg_simple_types])
            raise TypeError(f'You are adding an {arg_type} {arg} argument to op {cpp.name(f.func)} in addition to known types: '
                            f'{known_types_str}. Please update the list or materialize it so that it can be closed '
                            'over by value, also add a test in pytorch/xla/test/test_operations.py where this code '
                            'is exercised.')

        if arg_type == BaseCType(intArrayRefT):
            # It's not safe to close over IntArrayRef by value, since this is a
            # reference type, so materialize a vector to close over by value
            arg_vec = arg + '_vec'
            replay_view_func += ARRAYREF_TO_VEC.substitute(arg=arg, vec=arg_vec)
            updated_unpacked_args.append(arg_vec)
        elif arg_type == OptionalCType(BaseCType(longT)):
            # Materialize int64_t? to int64_t
            arg_value = arg + '_val'
            replay_view_func += OPTIONAL_TO_VAL.substitute(arg=arg, val=arg_value, default='0')
            updated_unpacked_args.append(arg_value)
        else:
            updated_unpacked_args.append(arg)

    replay_view_call = emit_view_call(f, input_base, updated_unpacked_args)
    replay_view_func += REPLAY_VIEW_LAMBDA_FUNC.substitute(
        input_base=input_base,
        replay_view_call=replay_view_call)

    is_view_with_metadata_change = 'true' if cpp.name(f.func) in VIEW_FUNCTIONS_WITH_METADATA_CHANGE else 'false'

    return SETUP_REPLAY_VIEW_IF_NOT_SUPPORT_AS_STRIDED_OR_VIEW_WITH_METADATA_CHANGE.substitute(
        is_view_with_metadata_change=is_view_with_metadata_change,
        replay_view_func=replay_view_func)
