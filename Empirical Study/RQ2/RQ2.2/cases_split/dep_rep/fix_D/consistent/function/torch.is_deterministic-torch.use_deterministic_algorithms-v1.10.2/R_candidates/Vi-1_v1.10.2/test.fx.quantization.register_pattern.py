def register_pattern(pattern):
    def insert(fn):
        DEFAULT_QUANTIZATION_PATTERNS[pattern] = fn
        return fn
    return insert
