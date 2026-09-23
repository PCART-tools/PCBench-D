def _dict_to_dataclass(cls, data):
    assert not isinstance(cls, str), f"Unresolved class type: '{cls}'."
    if typing.get_origin(cls) == Annotated:
        return _dict_to_dataclass(cls.__origin__, data)
    if typing.get_origin(cls) == typing.Union and type(None) in typing.get_args(cls):
        if data is None:
            return None
        ty_args = typing.get_args(cls)
        assert len(ty_args) == 2
        return _dict_to_dataclass(ty_args[0], data)
    elif isinstance(cls, type) and issubclass(cls, _Union):
        assert isinstance(data, dict)
        assert len(data) == 1
        _type = next(iter(data.keys()))
        _value = next(iter(data.values()))
        assert isinstance(_type, str)
        field_type = cls.__annotations__[_type]
        return cls.create(**{_type: _dict_to_dataclass(field_type, _value)})
    elif dataclasses.is_dataclass(cls):
        obj = cls(**data)  # type: ignore[assignment,operator]
        type_hints = typing.get_type_hints(cls)
        for f in dataclasses.fields(cls):
            name = f.name
            new_field_obj = _dict_to_dataclass(type_hints[name], getattr(obj, name))
            setattr(obj, name, new_field_obj)
        return obj
    elif isinstance(data, list):
        if len(data) == 0:
            return data
        d_type = typing.get_args(cls)[0]
        return [_dict_to_dataclass(d_type, d) for d in data]
    elif isinstance(data, dict):
        v_type = typing.get_args(cls)[1]
        return {k: _dict_to_dataclass(v_type, v) for k, v in data.items()}
    elif cls == float:
        return float(data)
    return data
