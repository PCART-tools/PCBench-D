def set_request_only(field):
    for f in field.all_scalars():
        categorical_limit, expected_value = None, None
        if not f.metadata:
            feature_specs = schema.FeatureSpec(feature_is_request_only=True)
        elif not f.metadata.feature_specs:
            categorical_limit = f.metadata.categorical_limit
            expected_value = f.metadata.expected_value
            feature_specs = schema.FeatureSpec(feature_is_request_only=True)
        else:
            categorical_limit = f.metadata.categorical_limit
            expected_value = f.metadata.expected_value
            feature_specs = schema.FeatureSpec(
                feature_type=f.metadata.feature_specs.feature_type,
                feature_names=f.metadata.feature_specs.feature_names,
                feature_ids=f.metadata.feature_specs.feature_ids,
                feature_is_request_only=True,
                desired_hash_size=f.metadata.feature_specs.desired_hash_size,
            )

        # make sure not to set categorical_limit for a non-integer field
        if not np.issubdtype(f.field_type(), np.integer):
            assert (
                categorical_limit is None
            ), "categorical_limit shouldn't be set for no-integer field"

        f.set_metadata(
            schema.Metadata(
                categorical_limit=categorical_limit,
                expected_value=expected_value,
                feature_specs=feature_specs,
            )
        )
