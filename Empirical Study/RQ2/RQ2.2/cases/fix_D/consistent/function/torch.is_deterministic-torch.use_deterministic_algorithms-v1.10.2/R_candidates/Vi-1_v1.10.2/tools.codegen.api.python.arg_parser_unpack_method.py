def arg_parser_unpack_method(t: Type, has_default: bool) -> str:
    if has_default and str(t) not in ('ScalarType', 'Device', 'Layout?'):
        raise RuntimeError(f'type \'{t}\' does not supported unpacking with default')

    if isinstance(t, BaseType):
        if t.name in [BaseTy.Tensor, BaseTy.Stream, BaseTy.Storage,
                      BaseTy.Scalar, BaseTy.Dimname]:
            # These unpack methods line up with their schema names
            return t.name.name.lower()
        elif t.name == BaseTy.ScalarType:
            return 'scalartypeWithDefault' if has_default else 'scalartype'
        elif t.name == BaseTy.Device:
            return 'deviceWithDefault' if has_default else 'device'
        elif t.name == BaseTy.int:
            return 'toInt64'
        elif t.name == BaseTy.bool:
            return 'toBool'
        elif t.name == BaseTy.float:
            return 'toDouble'
        elif t.name == BaseTy.str:
            return 'stringView'

    elif isinstance(t, OptionalType):
        if str(t.elem) == 'Tensor':
            return 'optionalTensor'

        elif isinstance(t.elem, BaseType):
            if t.elem.name in [BaseTy.ScalarType, BaseTy.Scalar,
                               BaseTy.int, BaseTy.bool,
                               BaseTy.float, BaseTy.str]:
                # Regular cases: append 'Optional' to elem's unpacking method
                return arg_parser_unpack_method(t.elem, False) + 'Optional'
            elif t.elem.name == BaseTy.MemoryFormat:
                return 'memoryformatOptional'
            elif t.elem.name == BaseTy.Generator:
                return 'generator'
            elif t.elem.name == BaseTy.Layout:
                return 'layoutWithDefault' if has_default else 'layoutOptional'
            elif t.elem.name == BaseTy.Device:
                return 'deviceWithDefault' if has_default else 'deviceOptional'

        elif isinstance(t.elem, ListType):
            if str(t.elem.elem) == 'int':
                # accept definite size
                return 'intlistOptional'
            elif str(t.elem) == 'float[]':
                return 'doublelistOptional'
            elif str(t.elem) == 'Dimname[]':
                return 'toDimnameListOptional'

    elif isinstance(t, ListType):
        if str(t.elem) == 'Tensor':
            # accept and use definite size
            if t.size is not None:
                return f'tensorlist_n<{t.size}>'
            else:
                return 'tensorlist'
        elif str(t.elem) == 'Tensor?':
            return 'list_of_optional_tensors'
        elif str(t.elem) == 'Dimname':
            # accept definite size
            return 'dimnamelist'
        elif str(t.elem) == 'int':
            # accept definite size
            return 'intlist'
        elif str(t) == 'float[]':
            return 'doublelist'
        elif str(t) == 'Scalar[]':
            return 'scalarlist'
    raise RuntimeError(f'type \'{t}\' is not supported by PythonArgParser')
