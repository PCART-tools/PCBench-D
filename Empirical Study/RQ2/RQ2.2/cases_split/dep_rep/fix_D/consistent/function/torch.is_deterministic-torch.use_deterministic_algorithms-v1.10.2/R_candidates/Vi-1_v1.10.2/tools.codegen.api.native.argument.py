def argument(a: Union[Argument, SelfArgument, TensorOptionsArguments], *, is_out: bool) -> List[Binding]:
    # Ideally, we NEVER default native functions.  However, there are a number
    # of functions that call native:: directly and rely on the defaulting
    # existing.  So for BC, we generate defaults for non-out variants (but not
    # for out variants, where it is impossible to generate an appropriate
    # default)
    should_default = not is_out
    if isinstance(a, Argument):
        default: Optional[str] = None
        if should_default and a.default is not None:
            default = cpp.default_expr(a.default, a.type)
        return [Binding(
            nctype=argument_type(a, binds=a.name),
            name=a.name,
            default=default,
            argument=a,
        )]
    elif isinstance(a, SelfArgument):
        # Erase SelfArgument from the distinction
        return argument(a.argument, is_out=is_out)
    elif isinstance(a, TensorOptionsArguments):
        default = None
        if should_default:
            default = '{}'
        # TODO: Not sure why the arguments assigned here are for
        # TensorOptionsArguments and not the constituent pieces.  It seems
        # to matter
        return [
            Binding(
                nctype=NamedCType('dtype', OptionalCType(BaseCType(scalarTypeT))),
                name='dtype',
                default=default,
                argument=a,
            ),
            Binding(
                nctype=NamedCType('layout', OptionalCType(BaseCType(layoutT))),
                name='layout',
                default=default,
                argument=a,
            ),
            Binding(
                nctype=NamedCType('device', OptionalCType(BaseCType(deviceT))),
                name='device',
                default=default,
                argument=a,
            ),
            Binding(
                nctype=NamedCType('pin_memory', OptionalCType(BaseCType(boolT))),
                name='pin_memory',
                default=default,
                argument=a,
            )]
    else:
        assert_never(a)
