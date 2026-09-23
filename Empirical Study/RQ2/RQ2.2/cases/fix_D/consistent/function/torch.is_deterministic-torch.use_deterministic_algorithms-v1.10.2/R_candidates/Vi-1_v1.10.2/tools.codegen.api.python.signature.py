def signature(f: NativeFunction, *, method: bool = False, pyi: bool = False) -> PythonSignature:
    args: List[Argument] = []
    args.extend(f.func.arguments.pre_self_positional)
    # Skip SelfArgument if this is method.
    if not method and f.func.arguments.self_arg is not None:
        args.append(f.func.arguments.self_arg.argument)
    args.extend(f.func.arguments.post_self_positional)
    args.extend(f.func.arguments.pre_tensor_options_kwarg_only)
    # Skip TensorOptionsArguments. Python side TensorOptions
    # arguments are created based on different rules - see below.
    args.extend(f.func.arguments.post_tensor_options_kwarg_only)
    args.extend(f.func.arguments.out)

    input_arg_set = set(a.name for a in f.func.arguments.flat_positional)
    kwarg_only_set = set(a.name for a in f.func.arguments.flat_kwarg_only)
    out_arg_set = set(a.name for a in f.func.arguments.out)

    input_args = tuple(map(argument, filter(lambda a: a.name in input_arg_set, args)))
    input_kwargs = tuple(map(argument, filter(lambda a: a.name in kwarg_only_set, args)))
    outputs = tuple(map(argument, filter(lambda a: a.name in out_arg_set, args)))

    # Reintroduce the scattered fields of TensorOptions for Python.
    # Compared to the cpp counterpart, the python arguments have new property
    # (default_init) and a new argument 'requires_grad', which require some
    # special handlings.
    # [old codegen] TODO: because these aren't guaranteed to be 100% faithful
    # to the original versions in the yaml, this recreation is a potential
    # source of drift between eager and JIT. Pull this logic out to a shared place.

    has_tensor_input_arg = any(a.type.is_tensor_like() for a in f.func.arguments.flat_non_out)
    if any(a.name == 'requires_grad' for a in f.func.schema_order_arguments()):
        raise ValueError('argument named requires_grad is reserved, should not explicitly add it in the schema')

    # [old codegen] this probably won't work if one of the returns is not a tensor,
    # but it will produce a compile-time error that is obvious.
    has_tensor_return = any(r.type.is_tensor_like() for r in f.func.returns)

    name: str = cpp.name(f.func)
    is_factory_function = f.category_override == 'factory' or (has_tensor_return and not has_tensor_input_arg)
    is_like_or_new_function = f.category_override in ('new', 'like') or name.startswith('new_') or name.endswith('_like')

    tensor_options_args: List[PythonArgument] = []
    if is_factory_function or is_like_or_new_function:
        tensor_options_args.append(PythonArgument(
            name='dtype',
            type=BaseType(BaseTy.ScalarType),
            default='None' if pyi else _dtype_default_type_hack(name),
            default_init='self.scalar_type()' if is_like_or_new_function else None,
        ))
        tensor_options_args.append(PythonArgument(
            name='layout',
            type=OptionalType(BaseType(BaseTy.Layout)),
            default='strided' if pyi else 'torch.strided',
            default_init='self.layout()' if is_like_or_new_function else None,
        ))
        tensor_options_args.append(PythonArgument(
            name='device',
            type=BaseType(BaseTy.Device),
            default='None',
            default_init='self.device()' if is_like_or_new_function else None,
        ))
        tensor_options_args.append(PythonArgument(
            name='pin_memory',
            type=BaseType(BaseTy.bool),
            default='False',
            default_init=None,
        ))
        tensor_options_args.append(PythonArgument(
            name='requires_grad',
            type=BaseType(BaseTy.bool),
            default='False',
            default_init=None,
        ))

    returns = PythonReturns(returns=f.func.returns)

    return PythonSignature(
        name=str(f.func.name.name),
        input_args=input_args,
        input_kwargs=input_kwargs,
        output_args=PythonOutArgument.from_outputs(outputs),
        tensor_options_args=tuple(tensor_options_args),
        returns=returns,
        method=method,
    )
