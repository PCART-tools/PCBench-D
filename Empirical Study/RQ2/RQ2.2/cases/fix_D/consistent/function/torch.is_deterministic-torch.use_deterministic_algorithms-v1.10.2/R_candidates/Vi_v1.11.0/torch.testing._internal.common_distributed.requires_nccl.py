def requires_nccl():
    return sandcastle_skip_if(
        not c10d.is_nccl_available(),
        "c10d was not compiled with the NCCL backend",
    )
