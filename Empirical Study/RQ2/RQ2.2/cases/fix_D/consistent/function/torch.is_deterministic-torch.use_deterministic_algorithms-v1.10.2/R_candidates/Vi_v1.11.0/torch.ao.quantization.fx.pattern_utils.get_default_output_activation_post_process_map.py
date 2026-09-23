def get_default_output_activation_post_process_map(is_training) -> Dict[Pattern, ObserverBase]:
    if is_training:
        return DEFAULT_OUTPUT_FAKE_QUANTIZE_MAP
    else:
        return DEFAULT_OUTPUT_OBSERVER_MAP
