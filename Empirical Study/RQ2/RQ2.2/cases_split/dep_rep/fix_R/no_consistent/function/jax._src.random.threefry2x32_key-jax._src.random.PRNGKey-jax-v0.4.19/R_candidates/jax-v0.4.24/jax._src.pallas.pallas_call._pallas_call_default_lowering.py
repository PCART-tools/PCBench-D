def _pallas_call_default_lowering(
    ctx: mlir.LoweringRuleContext,
    *in_nodes,
    interpret: bool,
    **params):
  platforms = ctx.module_context.platforms
  if len(platforms) > 1:
    raise ValueError("Can only lower pallas_call on a single platform.")
  platform = platforms[0]
  if interpret:
    # If we are in interpret mode, we don't care what platform we are on.
    impl = partial(_pallas_call_impl, **params, interpret=True)
    return mlir.lower_fun(impl, multiple_results=True)(ctx, *in_nodes)
  if platform == "cpu":
    # We only support interpret mode on the CPU backend.
    raise ValueError("Only interpret mode is supported on CPU backend.")
  # If we are actually using a specific backend (GPU or TPU), we should have
  # already registered backend-specific lowerings. If we get this far, it means
  # those backends aren't present.
  raise ValueError(
      f"Cannot lower pallas_call on platform: {platform}. "
      "To use Pallas on GPU, please install Triton and JAX-Triton. "
      "To use Pallas on TPU, please install Jaxlib TPU and libtpu.")
