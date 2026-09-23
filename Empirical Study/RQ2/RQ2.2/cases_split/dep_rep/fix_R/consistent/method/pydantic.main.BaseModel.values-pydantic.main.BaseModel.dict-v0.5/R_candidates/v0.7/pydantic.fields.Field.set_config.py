    def set_config(self, config):
        self.model_config = config
        field_config = _get_field_config(config, self.name)
        if field_config:
            self.alias = field_config.get('alias') or self.alias
            self.description = field_config.get('description') or self.description
