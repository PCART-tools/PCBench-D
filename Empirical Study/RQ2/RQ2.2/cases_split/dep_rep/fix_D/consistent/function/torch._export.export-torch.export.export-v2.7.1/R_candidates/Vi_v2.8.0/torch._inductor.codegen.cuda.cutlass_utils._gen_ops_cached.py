@clear_on_fresh_cache
@functools.cache
def _gen_ops_cached(arch, version) -> dict[Any, Any]:
    # Note: Cache needs to be specific for cuda architecture and version

    # Import cutlass python scripts.
    assert try_import_cutlass()
    import cutlass_library.generator as cutlass_generator
    import cutlass_library.manifest as cutlass_manifest

    if arch is None or version is None:
        log.error(
            "Cannot detect cuda arch %s or cuda version %s. "
            "Will discard all cutlass ops. "
            "Please consider setting _inductor.cuda.arch and _inductor.cuda.version configs.",
            arch,
            version,
        )
        return {}
    arch = _normalize_cuda_arch(arch)
    instantiation_level: str = config.cuda.cutlass_instantiation_level
    args = CUTLASSArgs(
        architectures=arch,
        cuda_version=version,
        instantiation_level=instantiation_level,
        operations=CUTLASS_OPERATION_KIND,
    )
    manifest = cutlass_manifest.Manifest(args)

    start_time = time.time()
    if arch == "100":
        if hasattr(cutlass_generator, "GenerateSM100"):
            cutlass_generator.GenerateSM100(manifest, args.cuda_version)
        cutlass_generator.GenerateSM90(manifest, args.cuda_version)
    else:
        try:
            func = getattr(cutlass_generator, "GenerateSM" + arch)
            func(manifest, args.cuda_version)
        except AttributeError as e:
            raise NotImplementedError(
                "Arch " + arch + " is not supported by current cutlass lib."
            ) from e

    log.info(
        "CUTLASS library generated a dict of %d operation kinds in %.2f seconds",
        len(manifest.operations),
        time.time() - start_time,
    )
    return manifest.operations
