    def __new__(mcs, name, bases, namespace):
        fields = {}
        config = BaseConfig
        for base in reversed(bases):
            if issubclass(base, BaseModel) and base != BaseModel:
                fields.update(base.__fields__)
                config = inherit_config(base.__config__, config)

        config = inherit_config(namespace.get('Config'), config)
        validators = _extract_validators(namespace)

        for f in fields.values():
            f.set_config(config)

        annotations = namespace.get('__annotations__', {})
        # annotation only fields need to come first in fields
        for ann_name, ann_type in annotations.items():
            if not ann_name.startswith('_') and ann_name not in namespace:
                fields[ann_name] = Field.infer(
                    name=ann_name,
                    value=...,
                    annotation=ann_type,
                    class_validators=_get_validators(validators, ann_name),
                    config=config,
                )

        for var_name, value in namespace.items():
            if not var_name.startswith('_') and not isinstance(value, TYPE_BLACKLIST):
                fields[var_name] = Field.infer(
                    name=var_name,
                    value=value,
                    annotation=annotations.get(var_name),
                    class_validators=_get_validators(validators, var_name),
                    config=config,
                )

        new_namespace = {
            '__config__': config,
            '__fields__': fields,
            '__validators__': validators,
            **{n: v for n, v in namespace.items() if n not in fields}
        }
        return super().__new__(mcs, name, bases, new_namespace)
