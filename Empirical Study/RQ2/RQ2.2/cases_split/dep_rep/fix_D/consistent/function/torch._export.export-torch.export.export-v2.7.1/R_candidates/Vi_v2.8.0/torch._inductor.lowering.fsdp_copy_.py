    @register_lowering(torch.ops.fsdp.copy_.default)
    def fsdp_copy_(dst, src):
        if dst is src:
            # dst.copy_(dst) can happen from the reinplacing pass
            return dst
        src = to_device(src, dst.get_device())
        src = to_dtype(src, dst.get_dtype())
        src = expand(src, dst.get_size())
        return mutate_to(dst, src)
