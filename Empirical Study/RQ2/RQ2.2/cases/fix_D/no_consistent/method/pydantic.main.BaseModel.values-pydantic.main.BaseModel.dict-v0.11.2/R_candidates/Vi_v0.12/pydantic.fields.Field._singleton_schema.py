    def _singleton_schema(self, by_alias):
        if self.sub_fields:
            if len(self.sub_fields) == 1:
                return self.sub_fields[0].type_schema(by_alias)
            else:
                return {
                    'type': 'any_of',
                    'types': [sf.type_schema(by_alias) for sf in self.sub_fields]
                }
        elif issubclass(self.type_, Enum):
            choice_names = self._schema.choice_names or {}
            return {
                'type': display_as_type(self.type_),
                'choices': [
                    (v.value, choice_names.get(v.value) or k.title())
                    for k, v in self.type_.__members__.items()
                ]
            }

        type_schema_method = getattr(self.type_, 'type_schema', None)
        if callable(type_schema_method):
            return type_schema_method(by_alias)
        else:
            return display_as_type(self.type_)
