def get_sparse_lookup_predictor_version(
    version,
    blob_size=None,
    min_blob_size_4bits=None,
    embedding_dim=None,
    sparse_feature_name=None,
):
    assert version in {
        'fp32', 'fp16', 'uint8rowwise', 'fused_uint8rowwise', 'fused_uint4rowwise'
    }, "Unexpected version of sparse_lookup layer {0}".format(version)
    if version == 'fused_uint4rowwise':
        if (
            blob_size is not None
            and min_blob_size_4bits is not None
            and embedding_dim is not None
        ):
            if blob_size < min_blob_size_4bits:
                logger.info(
                    "{} fall back to uint8 because lookup table size {} < min_blob_size_4bits {}".format(
                        sparse_feature_name,
                        blob_size,
                        min_blob_size_4bits,
                    )
                )
                version = 'fused_uint8rowwise'

            if embedding_dim % 2 == 1:
                logger.info(
                    "{} fall back to uint8 because lookup table dimension {} is not divisible by 2".format(
                        sparse_feature_name, embedding_dim
                    )
                )
                version = 'fused_uint8rowwise'
        else:
            raise ValueError(
                (
                    "When 4 bit quantization is enabled for {}, "
                    "(i.e., Sparse lookup predictor version:{}), "
                    "requires arguments blob_size:{}, "
                    "min_blob_size_4bits:{}, embedding_dim:{}"
                ).format(
                    sparse_feature_name,
                    version,
                    blob_size,
                    min_blob_size_4bits,
                    embedding_dim
                )
            )
    return version
