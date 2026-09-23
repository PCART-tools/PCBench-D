@register_lowering(
    aten.bucketize, type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.NO_OPMATH
)
def bucketize(
    input: TensorBox,
    boundaries: TensorBox,
    *,
    out_int32: bool = False,
    right: bool = False,
):
    assert len(boundaries.get_size()) == 1

    if not (
        V.graph.has_feature(input, BackendFeature.BUCKETIZE)
        and V.graph.has_feature(boundaries, BackendFeature.BUCKETIZE)
    ):
        return fallback_handler(aten.bucketize.Tensor, add_to_fallback_set=False)(
            input, boundaries, out_int32=out_int32, right=right
        )

    # The entire boundaries tensor needs to be used by ops.bucketize, so we
    # need to realize it into global memory; or in other words, we can't
    # guarantee that boundaries.get_name() (used below) will exist unless
    # we call boundaries.realize().
    boundaries.realize()
    device = input.get_device()
    input_loader = input.make_loader()

    index_dtype = torch.int32 if out_int32 else torch.int64

    def inner_fn(index):
        val = input_loader(index)
        indices = ops.bucketize(
            val,
            _boundaries_helper(boundaries),
            0,
            index_dtype,
            right,
        )

        return indices

    result = Pointwise.create(
        device=device,
        dtype=index_dtype,
        inner_fn=inner_fn,
        ranges=input.get_size(),
    )

    # [NOTE: inductor bucketize realize]
    # bucketize_binary_search is relatively expensive, so we don't want to re-compute
    # it unnecessarily. If we run bucketize() and then broadcast the result, we don't
    # want this to be fused into a large number of duplicate bucketize() computations
    # for each of the elements in the result.
    #
    # If no broadcasting occurs, fusions can still occur in scheduler.py
    result.realize()

    return result
