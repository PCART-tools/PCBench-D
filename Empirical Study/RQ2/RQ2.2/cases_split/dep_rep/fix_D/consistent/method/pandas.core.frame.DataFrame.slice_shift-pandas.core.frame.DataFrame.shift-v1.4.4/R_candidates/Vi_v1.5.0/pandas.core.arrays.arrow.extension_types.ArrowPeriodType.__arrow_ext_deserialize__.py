    @classmethod
    def __arrow_ext_deserialize__(cls, storage_type, serialized) -> ArrowPeriodType:
        metadata = json.loads(serialized.decode())
        return ArrowPeriodType(metadata["freq"])
