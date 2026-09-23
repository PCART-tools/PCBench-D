def check_memory_pool(
    device: int,
    pool_id: tuple[int, int],
    live_storages_ptrs: list[StorageWeakRefWrapper],
) -> None:
    assert all(isinstance(elem, StorageWeakRefWrapper) for elem in live_storages_ptrs)  # noqa: C419
    unique_storages = {stor.data_ptr() for stor in live_storages_ptrs if stor()}  # noqa: set_linter

    # check if there is a divergence first, then do the expensive snapshot call after
    # we know it will error
    if torch._C._cuda_checkPoolLiveAllocations(device, pool_id, unique_storages):
        return

    # at this point we are past the fast-path. we have seen rare cases where a dead tensor is dead,
    # but hasn't been gc'd yet, and gives false positive for allocated_not_in_live_storages
    gc.collect()
    torch.cuda.synchronize()

    segments = get_cudagraph_segments(pool_id)

    allocated_not_in_live_storages = {}

    for segment in segments:
        addr = segment["address"]
        for block in segment["blocks"]:
            if block["state"] == "active_allocated":
                if addr not in unique_storages:
                    allocated_not_in_live_storages[addr] = block
                else:
                    unique_storages.remove(addr)

            addr += block["size"]

    torch._check(
        len(unique_storages) == 0,
        lambda: f"These storage data ptrs are not allocated in pool {pool_id} but should be {unique_storages}",
    )

    if len(allocated_not_in_live_storages) != 0:
        formatted = []
        for dp, block in allocated_not_in_live_storages.items():
            trace = format_tb(block.get("frames", []))
            formatted.append(f"Data Pointer: {dp}, history: \n{trace}")
        formatted_s = "\n".join(formatted)
        msg = (
            f"These live storage data ptrs are in the cudagraph pool but not "
            f"accounted for as an output of cudagraph trees: \n\n{formatted_s}"
        )
        raise RuntimeError(msg)
