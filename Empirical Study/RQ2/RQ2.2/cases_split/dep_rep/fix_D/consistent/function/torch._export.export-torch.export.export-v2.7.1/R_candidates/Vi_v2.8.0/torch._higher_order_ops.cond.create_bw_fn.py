def create_bw_fn(fn: Callable, args: tuple[Any]) -> Callable:
    """
    For a fn that accepts flat inputs and returns flat outputs:
        fw_out = fn(*args),
    this function returns:
        grad_args = bw_fn(*args_and_grad_output)
    with the following invariants:
      1. args + fw_out has an 1-1 correspondence to args_and_grad_output
      2. grad_args has an 1-1 corresponsence to args
      3. for tensor arg whose requires_grad is False, its corresponding grad in
         grad_args will be a zero tensor with the same shape.
    """

    from torch._functorch.aot_autograd import AOTConfig, create_joint
    from torch._higher_order_ops.utils import prepare_fw_with_masks_all_requires_grad

    dummy_aot_config = AOTConfig(
        fw_compiler=None,  # type: ignore[arg-type]
        bw_compiler=None,  # type: ignore[arg-type]
        partition_fn=None,  # type: ignore[arg-type]
        decompositions={},
        num_params_buffers=0,
        aot_id=0,
        keep_inference_input_mutations=False,
    )
    n_primals = len(args)

    bw_fn = create_joint(
        prepare_fw_with_masks_all_requires_grad(fn), aot_config=dummy_aot_config
    )

    def flat_fn(*args_and_grad_outs):
        primals = args_and_grad_outs[:n_primals]
        tangents = args_and_grad_outs[n_primals:]
        grad_args = bw_fn(primals, tangents)[1]
        assert len(args) == len(grad_args)
        # In order to keep HOPs functional where the backward graph,
        # would have outputs that are aliasing inputs.
        # For example in cases where the backward of the function is simply
        # passing the upstream gradients through.
        maybe_clone = clone_outputs_aliasing_inputs(args_and_grad_outs)

        return [
            (
                torch.zeros_like(arg)
                if isinstance(arg, torch.Tensor) and grad is None
                else maybe_clone(grad)
            )
            for grad, arg in zip(grad_args, primals)
        ]

    return flat_fn
