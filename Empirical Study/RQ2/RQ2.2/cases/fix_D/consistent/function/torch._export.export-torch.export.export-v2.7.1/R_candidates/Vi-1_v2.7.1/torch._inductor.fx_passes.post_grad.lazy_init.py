@init_once_fakemode
def lazy_init():
    if torch._C._has_mkldnn:
        from . import decompose_mem_bound_mm  # noqa: F401
        from .mkldnn_fusion import _mkldnn_fusion_init

        _mkldnn_fusion_init()

    # Put this patterns in post-grad pass rather than joint-graph
    # pass since otherwise there will be perf/peak-memory regression:
    # https://github.com/pytorch/pytorch/issues/148141
    register_replacement(
        prepare_softmax_pattern,
        prepare_softmax_replacement,
        [torch.empty(4, 8)],
        scalar_workaround=dict(dim=-1),
        trace_fn=fwd_only,
        pass_dicts=pass_patterns[1],
        extra_check=prepare_softmax_extra_check,
    )
