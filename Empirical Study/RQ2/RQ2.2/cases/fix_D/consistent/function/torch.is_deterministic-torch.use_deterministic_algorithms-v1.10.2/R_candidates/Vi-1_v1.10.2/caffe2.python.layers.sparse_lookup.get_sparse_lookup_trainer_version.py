def get_sparse_lookup_trainer_version(version):
    assert version in {'fp32', 'fp16'},\
        "Unexpected version of sparse_lookup layer {0}".format(version)
    return version
