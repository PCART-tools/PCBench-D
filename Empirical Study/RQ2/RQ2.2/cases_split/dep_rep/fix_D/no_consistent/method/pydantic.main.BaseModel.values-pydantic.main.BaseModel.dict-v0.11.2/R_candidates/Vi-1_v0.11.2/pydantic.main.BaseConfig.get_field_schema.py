    @classmethod
    def get_field_schema(cls, name):
        field_config = cls.fields.get(name) or {}
        if isinstance(field_config, str):
            field_config = {'alias': field_config}
        return field_config
