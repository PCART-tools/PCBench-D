def argument(
    a: Union[Argument, TensorOptionsArguments, SelfArgument],
    *, cpp_no_default_args: Set[str], method: bool, faithful: bool,
    has_tensor_options: bool
) -> List[Binding]:
    def sub_argument(a: Union[Argument, TensorOptionsArguments, SelfArgument]) -> List[Binding]:
        return argument(
            a, cpp_no_default_args=cpp_no_default_args, method=method, faithful=faithful,
            has_tensor_options=has_tensor_options)

    if isinstance(a, Argument):
        binds: ArgName
        if a.name == "memory_format" and has_tensor_options:
            binds = SpecialArgName.possibly_redundant_memory_format
        else:
            binds = a.name
        default: Optional[str] = None
        if a.name not in cpp_no_default_args and a.default is not None:
            default = default_expr(a.default, a.type)
        return [Binding(
            nctype=argument_type(a, binds=binds),
            name=a.name,
            default=default,
            argument=a,
        )]
    elif isinstance(a, TensorOptionsArguments):
        if faithful:
            return sub_argument(a.dtype) + sub_argument(a.layout) + \
                sub_argument(a.device) + sub_argument(a.pin_memory)
        else:
            default = None
            # Enforced by NativeFunction.__post_init__
            assert 'options' not in cpp_no_default_args
            if all(x.default == "None" for x in a.all()):
                default = '{}'
            elif a.dtype.default == "long":
                default = 'at::kLong'  # TODO: this is wrong
            return [Binding(
                nctype=NamedCType('options', BaseCType(tensorOptionsT)),
                name='options',
                default=default,
                argument=a,
            )]
    elif isinstance(a, SelfArgument):
        if method:
            # Caller is responsible for installing implicit this in context!
            return []
        else:
            return sub_argument(a.argument)
    else:
        assert_never(a)
