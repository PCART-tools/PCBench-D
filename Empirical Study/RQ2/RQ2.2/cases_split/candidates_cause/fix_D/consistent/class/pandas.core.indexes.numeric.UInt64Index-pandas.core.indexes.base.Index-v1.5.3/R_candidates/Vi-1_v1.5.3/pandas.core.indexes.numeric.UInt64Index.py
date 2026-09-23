class UInt64Index(IntegerIndex):
    _index_descr_args = {
        "klass": "UInt64Index",
        "ltype": "unsigned integer",
        "dtype": "uint64",
        "extra": "",
    }
    __doc__ = _num_index_shared_docs["class_descr"] % _index_descr_args

    _typ = "uint64index"
    _default_dtype = np.dtype(np.uint64)
    _dtype_validation_metadata = (is_unsigned_integer_dtype, "unsigned integer")

    @property
    def _engine_type(self) -> type[libindex.UInt64Engine]:
        return libindex.UInt64Engine
