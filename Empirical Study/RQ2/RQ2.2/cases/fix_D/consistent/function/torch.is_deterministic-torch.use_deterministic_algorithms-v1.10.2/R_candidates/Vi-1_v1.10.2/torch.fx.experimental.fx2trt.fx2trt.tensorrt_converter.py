def tensorrt_converter(key):
    def register_converter(converter):
        CONVERTERS[key] = converter
        return converter

    return register_converter
