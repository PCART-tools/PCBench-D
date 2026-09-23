@clear_on_fresh_inductor_cache
@functools.lru_cache(None)
def _gen_ops_cached(arch, version) -> list[Any]:
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
        return []
    arch = _normalize_cuda_arch(arch)
    instantiation_level: str = config.cuda.cutlass_instantiation_level
    args = CUTLASSArgs(
        architectures=arch,
        cuda_version=version,
        instantiation_level=instantiation_level,
    )
    manifest = cutlass_manifest.Manifest(args)

    if arch == "100":
        try:
            from cutlass_generator import GenerateSM100  # type: ignore[import]

            GenerateSM100(manifest, args.cuda_version)
        except ImportError:
            log.warning("Cannot find GenerateSM100. Only GenerateSM90 will be used. ")
        cutlass_generator.GenerateSM90(manifest, args.cuda_version)
    elif arch == "90":
        cutlass_generator.GenerateSM90(manifest, args.cuda_version)
        cutlass_generator.GenerateSM80(manifest, args.cuda_version)
    else:
        try:
            func = getattr(cutlass_generator, "GenerateSM" + arch)
            func(manifest, args.cuda_version)
        except AttributeError as e:
            raise NotImplementedError(
                "Arch " + arch + " is not supported by current cutlass lib."
            ) from e
    return manifest.operations
