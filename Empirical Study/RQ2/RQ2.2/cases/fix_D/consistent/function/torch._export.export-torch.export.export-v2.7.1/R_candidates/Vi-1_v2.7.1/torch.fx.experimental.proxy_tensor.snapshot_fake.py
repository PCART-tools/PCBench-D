def snapshot_fake(val: Tensor) -> Optional[Tensor]:
    # val.detach() will also eventually call fast_detach(),
    # but this saves us a full trip into __torch_dispatch__
    # (snapshot_fake is called a lot)
    if isinstance(val, FakeTensor):
        return fast_detach(val.fake_mode, val)
    else:
        return val.detach()
