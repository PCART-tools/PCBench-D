@clear_on_fresh_cache
@functools.cache
def maybe_fetch_ops() -> Optional[list[Any]]:
    """
    Fetch ops from databases.
    """
    if config.force_disable_caches:
        return None

    # setup
    arch: str = get_cuda_arch()
    # get_cuda_version might return "12.4.0" or "12.4"
    # but we want to use "12.4"
    version: str = ".".join(get_cuda_version().split(".")[:2])
    instantiation_level: str = config.cuda.cutlass_instantiation_level

    # filename and filepath
    request_key: str = get_config_request_key(arch, version, instantiation_level)
    filename: str = _generate_config_filename(request_key)
    filepath: str = os.path.join(cache_dir(), filename)

    # try fetch
    serialized_ops: Optional[list[str]] = None
    start_time = time.time()
    if os.path.isfile(filepath):
        # locally
        try:
            with open(filepath) as f:
                serialized_ops = json.load(f)

            assert isinstance(serialized_ops, list), (
                f"Expected serialized ops is a list, got {type(serialized_ops)}"
            )
        except Exception as e:
            log.warning(
                "Failed to load CUTLASS config %s from local cache: %s",
                filename,
                e,
            )
            serialized_ops = None
    elif config.is_fbcode():
        from torch._inductor.fb.cutlass_remote_cache import (
            maybe_fetch_cutlass_configs_from_remote,
        )

        # from remote
        serialized_ops = maybe_fetch_cutlass_configs_from_remote(filepath)

    if serialized_ops is None:
        return None

    # deserialize
    serializer = get_cutlass_operation_serializer()
    full_ops = [serializer.deserialize(x) for x in serialized_ops]  # type: ignore[union-attr]
    log.info("Loaded ops from %s cache in %.3fs", filename, time.time() - start_time)
    return full_ops
