class Float64Index(NumericIndex):
    _index_descr_args = {
        "klass": "Float64Index",
        "dtype": "float64",
        "ltype": "float",
        "extra": "",
    }
    __doc__ = _num_index_shared_docs["class_descr"] % _index_descr_args

    _typ = "float64index"
    _engine_type = libindex.Float64Engine
    _default_dtype = np.dtype(np.float64)
    _dtype_validation_metadata = (is_float_dtype, "float")
