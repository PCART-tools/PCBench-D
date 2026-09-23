    @classmethod
    def infer(cls, *, name, value, annotation, class_validators, config):
        required = value == Required
        field_config = _get_field_config(config, name)
        return cls(
            name=name,
            type_=annotation,
            alias=field_config and field_config.get('alias'),
            class_validators=class_validators,
            default=None if required else value,
            required=required,
            model_config=config,
            description=field_config and field_config.get('description'),
        )
