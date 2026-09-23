def gen_create_out_helper(backend_index: BackendIndex) -> List[str]:
    if backend_index.dispatch_key == DispatchKey.Meta:
        empty_options = "options.device(at::kMeta)"
    else:
        empty_options = "options"

    if backend_index.dispatch_key in (
            DispatchKey.Meta, DispatchKey.CPU, DispatchKey.CUDA):
        dispatch = str(backend_index.dispatch_key).lower()
        empty_impl = f"at::detail::empty_{dispatch}"
        empty_strided_impl = f"at::detail::empty_strided_{dispatch}"
        runtime_empty_supported_check = ""
    elif backend_index.dispatch_key == DispatchKey.CompositeExplicitAutograd:
        empty_impl = "at::empty"
        empty_strided_impl = "at::empty_strided"
        runtime_empty_supported_check = """\
  if (!c10::detail::backend_supports_empty_operator(options)) {{
    // The main purpose of this CompositeExplicitAutograd kernel is to provide
    // a "free" implementation of out-of-place operators.
    // If a backend hasn't implemented an out-of-place op but has implemented
    // the out= variant, then this kernel will call their out= variant.
    // It does that by using at::empty() to create the tensor to pass to the out= variant though,
    // so this "default" kernel doesn't actually handle backends that don't support at::empty
    // (e.g. quantized backends).
    // Returning an undefined tensor here allows us to reach the out= kernel and give a better error.
    // Longer term, this could be better fixed by https://github.com/pytorch/pytorch/issues/52680
    return at::Tensor();
  }}
"""
    else:
        return []

    return [f"""
Tensor create_out(IntArrayRef sizes, IntArrayRef strides, const TensorOptions &options) {{
  {runtime_empty_supported_check}
  if (strides.empty()) {{
      return {empty_impl}(sizes, {empty_options});
  }} else {{
      return {empty_strided_impl}(sizes, strides, {empty_options});
  }}
}}
"""]
