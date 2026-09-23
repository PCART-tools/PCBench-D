def requires_nccl_version(version, msg):
    if not c10d.is_nccl_available():
        return sandcastle_skip(
            "c10d was not compiled with the NCCL backend",
        )
    else:
        return sandcastle_skip_if(
            torch.cuda.nccl.version() < version,
            "Requires NCCL version greater than or equal to: {}, found: {}, reason: {}".format(
                version, torch.cuda.nccl.version(), msg
            ),
        )
