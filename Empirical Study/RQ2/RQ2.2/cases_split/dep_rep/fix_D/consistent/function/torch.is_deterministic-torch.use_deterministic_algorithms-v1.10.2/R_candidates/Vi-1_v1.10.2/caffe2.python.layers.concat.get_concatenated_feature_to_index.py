def get_concatenated_feature_to_index(blobs_to_concat):
    concat_feature_to_index = defaultdict(list)
    start_pos = 0
    for scalar in blobs_to_concat:
        num_dims = scalar.dtype.shape[0]
        if hasattr(scalar, 'metadata') \
            and hasattr(scalar.metadata, 'feature_specs') \
            and hasattr(scalar.metadata.feature_specs, 'feature_to_index') \
                and isinstance(scalar.metadata.feature_specs.feature_to_index, dict):  # noqa B950
            for k, v in scalar.metadata.feature_specs.feature_to_index.items():
                concat_feature_to_index[k].extend([start_pos + vi for vi in v])
        start_pos += num_dims
    return dict(concat_feature_to_index) if concat_feature_to_index.keys() else None
