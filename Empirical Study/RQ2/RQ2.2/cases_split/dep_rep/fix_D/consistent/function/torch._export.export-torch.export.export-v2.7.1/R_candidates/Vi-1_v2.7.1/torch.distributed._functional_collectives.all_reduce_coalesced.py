def all_reduce_coalesced(
    self: list[torch.Tensor], reduceOp: str, group: RANK_TYPES, tag: str = ""
) -> list[torch.Tensor]:
    """
    Reduces a list of tensors across all machines in such a way that all get
    the final result.

    The all tensors in the input list are left unmodified.

    Group can be one of:
        List[int]: ranks participating in the collective.
        List[List[int]]: 2D mesh of ranks taking part of this collective in MPMD.
        ProcessGroup: Will perform a collective using the ranks and tag of the PG.
        DeviceMesh: Do a SPMD collective over all ranks of the mesh
        (DeviceMesh, int): Do a MPMD collective over one dimension of the DeviceMesh

    :: N.B. If you pass a PG or a 1D list to perform a MPMD collective, the compiler won't be able to recover
    that information and perform collective algebraic optimization. Use other forms of input for that.
    """
    group_name = _resolve_group_name(group, tag)
    tensor_list = torch.ops._c10d_functional.all_reduce_coalesced(  # type: ignore[attr-defined]
        self,
        reduceOp.lower(),
        group_name,
    )
    return list(map(_maybe_wrap_tensor, tensor_list))
