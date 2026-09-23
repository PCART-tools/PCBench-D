def gen_inplace_or_view_type(
    out: str,
    native_yaml_path: str,
    fns_with_infos: List[NativeFunctionWithDifferentiabilityInfo],
    template_path: str
) -> None:
    # NOTE: see Note [Sharded File] at the top of the VariableType.cpp
    # template regarding sharding of the generated files.
    num_shards = 2
    shards: List[List[NativeFunctionWithDifferentiabilityInfo]] = [[] for _ in range(num_shards)]

    # functions are assigned arbitrarily but stably to a file based on hash
    for fn in fns_with_infos:
        x = sum(ord(c) for c in cpp.name(fn.func.func)) % num_shards
        shards[x].append(fn)

    fm = FileManager(install_dir=out, template_dir=template_path, dry_run=False)
    for i, shard in enumerate(shards):
        gen_inplace_or_view_type_shard(fm, shard, f'_{i}')
    gen_inplace_or_view_type_shard(fm, fns_with_infos, 'Everything')
