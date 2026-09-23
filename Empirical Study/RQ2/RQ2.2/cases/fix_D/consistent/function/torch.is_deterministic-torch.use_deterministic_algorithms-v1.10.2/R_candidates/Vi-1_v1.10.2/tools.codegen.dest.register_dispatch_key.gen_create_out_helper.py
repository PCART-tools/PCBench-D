def gen_create_out_helper(backend_index: BackendIndex) -> List[str]:
    if backend_index.dispatch_key == DispatchKey.Meta:
        # TODO: dedupe this with below
        core = """
if (strides.empty()) {
    return at::empty(sizes, options.device(at::kMeta));
} else {
    return at::empty_strided(sizes, strides, options.device(at::kMeta));
}
"""
    else:
        expanded_topts = "optTypeMetaToScalarType(options.dtype_opt()), options.layout_opt(), " \
            "options.device_opt(), options.pinned_memory_opt()"
        empty_init = ""
        if backend_index.dispatch_key == DispatchKey.CPU:
            empty_impl = "at::native::empty_cpu"
            empty_strided_impl = "at::native::empty_strided_cpu"
        elif backend_index.dispatch_key == DispatchKey.CUDA:
            empty_init = "globalContext().lazyInitCUDA();"
            empty_impl = "at::native::empty_cuda"
            empty_strided_impl = "at::native::empty_strided_cuda"
        elif backend_index.dispatch_key == DispatchKey.CompositeExplicitAutograd:
            empty_impl = "at::empty"
            empty_strided_impl = "at::empty_strided"
        else:
            return []
        core = f"""
  {empty_init}
  if (strides.empty()) {{
      return {empty_impl}(sizes, {expanded_topts}, options.memory_format_opt());
  }} else {{
      // TODO: assert options.memory_format_opt() is nullopt (debug only?)
      return {empty_strided_impl}(sizes, strides, {expanded_topts});
  }}
"""
    return [f"""
Tensor create_out(IntArrayRef sizes, IntArrayRef strides, const TensorOptions &options) {{
{core}
}}
"""]
