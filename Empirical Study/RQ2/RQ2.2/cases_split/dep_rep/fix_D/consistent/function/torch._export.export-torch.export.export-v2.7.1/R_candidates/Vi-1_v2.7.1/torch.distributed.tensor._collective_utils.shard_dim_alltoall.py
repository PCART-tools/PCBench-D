def shard_dim_alltoall(input, gather_dim, shard_dim, mesh, mesh_dim):
    if mesh.device_type == "cpu":
        # Gloo does not support alltoall, so falling back to allgather + chunk

        # TODO: This logs way too much
        logger.warning(
            "CPU process group does not support alltoall yet, falling back with allgather + chunk!"
        )
        out = funcol.all_gather_tensor(input, gather_dim, (mesh, mesh_dim))
        if isinstance(out, funcol.AsyncCollectiveTensor):
            # stick to the same behavior for the alltoall case, remove this once we enable alltoall async
            out = out.wait()
        out = torch.chunk(out, mesh.size(mesh_dim), dim=shard_dim)[
            mesh.get_local_rank(mesh_dim)
        ]
        return out.contiguous()

    group_name = funcol._resolve_group_name((mesh, mesh_dim))
    # TODO: enable async op for shard_dim_alltoall
    return torch.ops._dtensor.shard_dim_alltoall(
        input, gather_dim, shard_dim, group_name
    )
