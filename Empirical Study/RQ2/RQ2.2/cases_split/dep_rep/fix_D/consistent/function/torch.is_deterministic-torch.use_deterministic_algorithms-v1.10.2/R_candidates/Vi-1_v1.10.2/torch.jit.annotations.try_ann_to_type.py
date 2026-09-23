def try_ann_to_type(ann, loc):
    if ann is inspect.Signature.empty:
        return TensorType.getInferred()
    if ann is None:
        return NoneType.get()
    if inspect.isclass(ann) and is_tensor(ann):
        return TensorType.get()
    if is_tuple(ann):
        # Special case for the empty Tuple type annotation `Tuple[()]`
        if len(ann.__args__) == 1 and ann.__args__[0] == ():
            return TupleType([])
        return TupleType([try_ann_to_type(a, loc) for a in ann.__args__])
    if is_list(ann):
        elem_type = try_ann_to_type(ann.__args__[0], loc)
        if elem_type:
            return ListType(elem_type)
    if is_dict(ann):
        key = try_ann_to_type(ann.__args__[0], loc)
        value = try_ann_to_type(ann.__args__[1], loc)
        # Raise error if key or value is None
        if key is None:
            raise ValueError(f"Unknown type annotation: '{ann.__args__[0]}' at {loc.highlight()}")
        if value is None:
            raise ValueError(f"Unknown type annotation: '{ann.__args__[1]}' at {loc.highlight()}")
        return DictType(key, value)
    if is_optional(ann):
        if issubclass(ann.__args__[1], type(None)):
            contained = ann.__args__[0]
        else:
            contained = ann.__args__[1]
        valid_type = try_ann_to_type(contained, loc)
        msg = "Unsupported annotation {} could not be resolved because {} could not be resolved."
        assert valid_type, msg.format(repr(ann), repr(contained))
        return OptionalType(valid_type)
    if is_union(ann):
        inner: List = []
        # We need these extra checks because both `None` and invalid
        # values will return `None`
        # TODO: Determine if the other cases need to be fixed as well
        for a in ann.__args__:
            if a is None:
                inner.append(NoneType.get())
            maybe_type = try_ann_to_type(a, loc)
            msg = "Unsupported annotation {} could not be resolved because {} could not be resolved."
            assert maybe_type, msg.format(repr(ann), repr(maybe_type))
            inner.append(maybe_type)
        return UnionType(inner)    # type: ignore[arg-type]
    if torch.distributed.rpc.is_available() and is_rref(ann):
        return RRefType(try_ann_to_type(ann.__args__[0], loc))
    if is_future(ann):
        return FutureType(try_ann_to_type(ann.__args__[0], loc))
    if ann is float:
        return FloatType.get()
    if ann is complex:
        return ComplexType.get()
    if ann is int:
        return IntType.get()
    if ann is str:
        return StringType.get()
    if ann is bool:
        return BoolType.get()
    if ann is Any:
        return AnyType.get()
    if ann is type(None):
        return NoneType.get()
    if inspect.isclass(ann) and hasattr(ann, "__torch_script_interface__"):
        return InterfaceType(ann.__torch_script_interface__)
    if ann is torch.device:
        return DeviceObjType.get()
    if ann is torch.Stream:
        return StreamObjType.get()
    if ann is torch.dtype:
        return IntType.get()  # dtype not yet bound in as its own type
    if inspect.isclass(ann) and issubclass(ann, enum.Enum):
        if _get_script_class(ann) is None:
            scripted_class = torch.jit._script._recursive_compile_class(ann, loc)
            name = scripted_class.qualified_name()
        else:
            name = _qualified_name(ann)
        return EnumType(name, get_enum_value_type(ann, loc), list(ann))
    if inspect.isclass(ann):
        maybe_script_class = _get_script_class(ann)
        if maybe_script_class is not None:
            return maybe_script_class
        if torch._jit_internal.can_compile_class(ann):
            return torch.jit._script._recursive_compile_class(ann, loc)

    # Maybe resolve a NamedTuple to a Tuple Type
    def fake_rcb(key):
        return None
    return torch._C._resolve_type_from_object(ann, loc, fake_rcb)
