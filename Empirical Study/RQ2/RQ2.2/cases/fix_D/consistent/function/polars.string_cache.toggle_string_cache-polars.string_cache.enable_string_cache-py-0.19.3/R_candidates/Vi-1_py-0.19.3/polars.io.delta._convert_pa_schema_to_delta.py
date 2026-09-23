def _convert_pa_schema_to_delta(schema: pa.schema) -> pa.schema:
    """Convert a PyArrow schema to a schema compatible with Delta Lake."""
    # TODO: Add time zone support
    dtype_map = {
        pa.uint8(): pa.int8(),
        pa.uint16(): pa.int16(),
        pa.uint32(): pa.int32(),
        pa.uint64(): pa.int64(),
        pa.large_string(): pa.string(),
        pa.large_binary(): pa.binary(),
    }

    def dtype_to_delta_dtype(dtype: pa.DataType) -> pa.DataType:
        # Handle nested types
        if isinstance(dtype, pa.LargeListType):
            return list_to_delta_dtype(dtype)
        elif isinstance(dtype, pa.StructType):
            return struct_to_delta_dtype(dtype)
        elif isinstance(dtype, pa.TimestampType):
            # TODO: Support time zones when implemented by delta-rs. See:
            # https://github.com/delta-io/delta-rs/issues/1598
            return pa.timestamp("us")
        try:
            return dtype_map[dtype]
        except KeyError:
            return dtype

    def list_to_delta_dtype(dtype: pa.LargeListType) -> pa.ListType:
        nested_dtype = dtype.value_type
        nested_dtype_cast = dtype_to_delta_dtype(nested_dtype)
        return pa.list_(nested_dtype_cast)

    def struct_to_delta_dtype(dtype: pa.StructType) -> pa.StructType:
        fields = [dtype.field(i) for i in range(dtype.num_fields)]
        fields_cast = [pa.field(f.name, dtype_to_delta_dtype(f.type)) for f in fields]
        return pa.struct(fields_cast)

    return pa.schema([pa.field(f.name, dtype_to_delta_dtype(f.type)) for f in schema])
