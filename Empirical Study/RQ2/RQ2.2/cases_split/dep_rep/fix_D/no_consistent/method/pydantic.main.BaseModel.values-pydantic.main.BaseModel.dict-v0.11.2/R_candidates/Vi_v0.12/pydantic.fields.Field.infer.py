    @classmethod
    def infer(cls, *, name, value, annotation, class_validators, config):
        schema_from_config = config.get_field_schema(name)
        if isinstance(value, Schema):
            schema = value
            value = schema.default
        else:
            schema = Schema(value, **schema_from_config)
        schema.alias = schema.alias or schema_from_config.get('alias')
        required = value == Required
        return cls(
            name=name,
            type_=annotation,
            alias=schema.alias,
            class_validators=class_validators,
            default=None if required else value,
            required=required,
            model_config=config,
            schema=schema,
        )
