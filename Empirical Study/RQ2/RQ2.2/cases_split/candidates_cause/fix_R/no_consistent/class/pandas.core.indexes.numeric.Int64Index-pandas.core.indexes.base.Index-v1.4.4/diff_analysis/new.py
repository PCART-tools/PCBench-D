class Int64Index(IntegerIndex):
    _index_descr_args = {
        "klass": "Int64Index",
        "ltype": "integer",
        "dtype": "int64",
        "extra": "",
    }
    __doc__ = _num_index_shared_docs["class_descr"] % _index_descr_args

    _typ = "int64index"
    _default_dtype = np.dtype(np.int64)
    _dtype_validation_metadata = (is_signed_integer_dtype, "signed integer")

    @property
    def _engine_type(self) -> type[libindex.Int64Engine]:
        return libindex.Int64Engine
