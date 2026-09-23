def get_cache_key() -> Optional[str]:
    # TODO: info versions of these logs that log only once
    if torch._inductor.config.force_disable_caches:
        warn_once(
            "dynamo_pgo force disabled by torch._inductor.config.force_disable_caches"
        )
        return None

    # NB: We always use global rank for keys, even though they are overkill
    # for local only cache
    rank = None
    if dist.is_available() and dist.is_initialized():
        rank = dist.get_rank()

    tag = torch.compiler.config.cache_key_tag

    # NB: We namespace the cache keys so that only user-specified job id
    # can alias with each other.
    if (r := torch.compiler.config.job_id) is not None:
        if r.startswith("mast:"):
            raise ReservedWorkflowIdUserError(
                "torch.compiler.config.job_id with prefix 'mast:' is reserved for "
                "automatically generated job id associated with a specific MAST job "
                "name and version."
            )
        return f"{r}:{rank}:{tag}"

    if (name_version := torch._utils_internal.get_mast_job_name_version()) is not None:
        mast_job_name, mast_job_version = name_version
        return f"mast:{mast_job_name}:{mast_job_version}:{rank}:{tag}"

    return None
