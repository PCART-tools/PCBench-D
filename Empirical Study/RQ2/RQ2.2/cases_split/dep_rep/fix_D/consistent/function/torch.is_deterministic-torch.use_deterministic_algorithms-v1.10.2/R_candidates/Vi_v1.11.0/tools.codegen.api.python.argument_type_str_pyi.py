def argument_type_str_pyi(t: Type) -> str:
    add_optional = False
    if isinstance(t, OptionalType):
        t = t.elem
        add_optional = True

    if isinstance(t, BaseType):
        if t.name == BaseTy.int:
            ret = '_int'
        elif t.name == BaseTy.float:
            ret = '_float'
        elif t.name == BaseTy.str:
            ret = 'str'
        elif t.name == BaseTy.Scalar:
            ret = 'Number'
        elif t.name == BaseTy.ScalarType:
            ret = '_dtype'
        elif t.name == BaseTy.bool:
            ret = '_bool'
        elif t.name == BaseTy.QScheme:
            ret = '_qscheme'
        elif t.name == BaseTy.Layout:
            ret = '_layout'
        elif t.name == BaseTy.Device:
            ret = 'Union[_device, str, None]'
        elif t.name == BaseTy.MemoryFormat:
            ret = 'memory_format'
        elif t.name == BaseTy.Dimname:
            ret = 'Union[str, ellipsis, None]'
        elif t.name in [BaseTy.Tensor, BaseTy.Generator,
                        BaseTy.Storage, BaseTy.Stream]:
            # These python schema type names line up with their function schema names
            ret = t.name.name

    elif isinstance(t, ListType):
        if str(t.elem) == 'int':
            ret = 'Union[_int, _size]' if t.size is not None else '_size'
        elif t.is_tensor_like():
            # TODO: this doesn't seem right...
            # Tensor?[] currently translates to Optional[Union[Tuple[Tensor, ...], List[Tensor]]]
            # It should probably translate to   Union[Tuple[Optional[Tensor], ...], List[Optional[Tensor]]]
            if isinstance(t.elem, OptionalType):
                add_optional = True
            ret = 'Union[Tensor, Tuple[Tensor, ...], List[Tensor]]' if t.size is not None else \
                  'Union[Tuple[Tensor, ...], List[Tensor]]'
        elif str(t.elem) == 'float':
            ret = 'Sequence[_float]'
        else:
            elem = argument_type_str_pyi(t.elem)
            ret = f'Sequence[{elem}]'

    if add_optional:
        ret = 'Optional[' + ret + ']'
    return ret

    raise RuntimeError(f'unrecognized type {repr(t)}')
