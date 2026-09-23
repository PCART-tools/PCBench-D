    def __init__(self, subtype, closed):
        # attributes need to be set first before calling
        # super init (as that calls serialize)
        assert closed in VALID_CLOSED
        self._closed = closed
        if not isinstance(subtype, pyarrow.DataType):
            subtype = pyarrow.type_for_alias(str(subtype))
        self._subtype = subtype

        storage_type = pyarrow.struct([("left", subtype), ("right", subtype)])
        pyarrow.ExtensionType.__init__(self, storage_type, "pandas.interval")
