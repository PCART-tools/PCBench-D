def register_quant_pattern(pattern, output_activation_post_process=None):
    def insert(fn):
        DEFAULT_QUANTIZATION_PATTERNS[pattern] = fn
        if output_activation_post_process is not None:
            DEFAULT_OUTPUT_ACTIVATION_POST_PROCESS_MAP[pattern] = output_activation_post_process
        return fn
    return insert
