    @classmethod
    def type_schema(cls, by_alias):
        return {
            'type': 'object',
            'properties': (
                {f.alias: f.schema(by_alias) for f in cls.__fields__.values()}
                if by_alias else
                {k: f.schema(by_alias) for k, f in cls.__fields__.items()}
            )
        }
