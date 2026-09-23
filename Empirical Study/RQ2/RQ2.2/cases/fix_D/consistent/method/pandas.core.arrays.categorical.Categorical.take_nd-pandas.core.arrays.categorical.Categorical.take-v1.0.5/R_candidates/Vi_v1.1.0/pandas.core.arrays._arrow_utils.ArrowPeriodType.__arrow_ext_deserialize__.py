        @classmethod
        def __arrow_ext_deserialize__(cls, storage_type, serialized):
            metadata = json.loads(serialized.decode())
            return ArrowPeriodType(metadata["freq"])
