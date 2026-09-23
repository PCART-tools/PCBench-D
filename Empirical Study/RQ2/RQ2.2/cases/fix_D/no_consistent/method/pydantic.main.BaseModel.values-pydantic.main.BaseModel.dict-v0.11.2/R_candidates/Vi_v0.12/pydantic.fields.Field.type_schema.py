    def type_schema(self, by_alias):
        if self.shape is Shape.LIST:
            return {
                'type': 'list',
                'item_type': self._singleton_schema(by_alias),
            }
        if self.shape is Shape.SET:
            return {
                'type': 'set',
                'item_type': self._singleton_schema(by_alias),
            }
        elif self.shape is Shape.MAPPING:
            return {
                'type': 'mapping',
                'item_type': self._singleton_schema(by_alias),
                'key_type': self.key_field.type_schema(by_alias)
            }
        elif self.shape is Shape.TUPLE:
            return {
                'type': 'tuple',
                'item_types': [sf.type_schema(by_alias) for sf in self.sub_fields],
            }
        else:
            assert self.shape is Shape.SINGLETON, self.shape
            return self._singleton_schema(by_alias)
