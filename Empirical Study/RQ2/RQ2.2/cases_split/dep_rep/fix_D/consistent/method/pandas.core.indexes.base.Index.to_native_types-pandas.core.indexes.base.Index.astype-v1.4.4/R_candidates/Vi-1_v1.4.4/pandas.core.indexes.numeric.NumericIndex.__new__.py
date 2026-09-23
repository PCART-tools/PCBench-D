    def __new__(cls, data=None, dtype: Dtype | None = None, copy=False, name=None):
        name = maybe_extract_name(name, data, cls)

        subarr = cls._ensure_array(data, dtype, copy)
        return cls._simple_new(subarr, name=name)
