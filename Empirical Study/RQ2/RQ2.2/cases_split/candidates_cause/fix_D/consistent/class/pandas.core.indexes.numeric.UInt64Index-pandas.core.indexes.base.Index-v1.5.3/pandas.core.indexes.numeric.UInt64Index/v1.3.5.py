class UInt64Index(IntegerIndex):
    _index_descr_args = {
        "klass": "UInt64Index",
        "ltype": "unsigned integer",
        "dtype": "uint64",
        "extra": "",
    }
    __doc__ = _num_index_shared_docs["class_descr"] % _index_descr_args

    _typ = "uint64index"
    _engine_type = libindex.UInt64Engine
    _default_dtype = np.dtype(np.uint64)
    _dtype_validation_metadata = (is_unsigned_integer_dtype, "unsigned integer")

    def _validate_fill_value(self, value):
        # e.g. np.array([1]) we want np.array([1], dtype=np.uint64)
        #  see test_where_uin64
        super()._validate_fill_value(value)
        if hasattr(value, "dtype") and is_signed_integer_dtype(value.dtype):
            if (value >= 0).all():
                return value.astype(self.dtype)
            raise TypeError
        return value
