def _set_numpy_to_constructor() -> None:
    global _NUMPY_TYPE_TO_CONSTRUCTOR
    _NUMPY_TYPE_TO_CONSTRUCTOR = {
        np.float32: PySeries.new_f32,
        np.float64: PySeries.new_f64,
        np.int8: PySeries.new_i8,
        np.int16: PySeries.new_i16,
        np.int32: PySeries.new_i32,
        np.int64: PySeries.new_i64,
        np.uint8: PySeries.new_u8,
        np.uint16: PySeries.new_u16,
        np.uint32: PySeries.new_u32,
        np.uint64: PySeries.new_u64,
        np.str_: PySeries.new_str,
        np.bytes_: PySeries.new_binary,
        np.bool_: PySeries.new_bool,
        np.datetime64: PySeries.new_i64,
    }
