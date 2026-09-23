    def set_config(self, config):
        self.model_config = config
        schema_from_config = config.get_field_schema(self.name)
        if schema_from_config:
            self._schema.alias = self._schema.alias or schema_from_config.get('alias')
            self.alias = self._schema.alias
