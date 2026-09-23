def emit_view_functionalization_body(
        f: NativeFunction,
        functional_op: NativeFunction
) -> str:
    # view op case
    assert f.is_view_op

    if f.tag is Tag.inplace_view:
        # This op is both an inplace op AND a view op.
        # See Note [Functionalization Pass - Inplace View Ops] for details.
        # I currently have the view meta call into the out-of-place variant of the view, to avoid
        # having to define an extra ~20 inplace {view}_inverse_ functions.
        # Most view ops don't have NativeFunctionGroup's both, because we don't define out= variants for view ops.
        # I'm assuming that every inplace-view op has a corresponding out-of-place view op,
        # with the same name but the trailing underscore removed.
        # This is currently asserted at parse time in gen.py (see error_check_native_functions).
        assert f.func.kind() is SchemaKind.inplace
        # Requirement: Every inplace_view op needs to have a corresponding functional view op, which we paired together beforehand.
        assert functional_op is not None
        api_name = functional_op.func.name.unambiguous_name()
        call_sig = DispatcherSignature.from_schema(functional_op.func)
    else:
        api_name = f.func.name.unambiguous_name()
        call_sig = DispatcherSignature.from_schema(f.func)

    dispatcher_sig = DispatcherSignature.from_schema(f.func)
    assert_view_op_properties(f.func)
    view_tensor_name = dispatcher_sig.arguments()[0].name

    keyset = 'dispatchKeySet & c10::after_func_keyset'
    return_type = dispatcher_sig.returns_type().remove_const_ref().cpp_type()

    unwrap_tensor_args_str, unwrapped_args_ctx = unwrap_tensor_args(dispatcher_sig)
    view_redispatch_args = [keyset] + [e.expr for e in translate(unwrapped_args_ctx, call_sig.arguments(), method=False)]

    forward_lambda = FunctionalizationLambda.from_func(f, functional_op=functional_op, is_reverse=False)
    reverse_lambda = FunctionalizationLambda.from_func(f, functional_op=functional_op, is_reverse=True)

    # The meta API call should use the same arguments, but convert all tensors to meta tensors first.
    meta_conversion_str, meta_call_ctx = convert_to_meta_tensors(dispatcher_sig)
    meta_call_args = [e.expr for e in translate(meta_call_ctx, call_sig.arguments(), method=False)]

    if f.tag is Tag.inplace_view:
        # See Note [Functionalization Pass - Inplace View Ops] for more details
        return f"""
      at::functionalization::ViewMeta view_meta = at::functionalization::ViewMeta(
        {forward_lambda.decl()} {{
          return {forward_lambda.inner_call()}
        }},
        {reverse_lambda.decl()} {{
          return {reverse_lambda.inner_call()}
        }}
      );
      at::functionalization::impl::mutate_view_meta({view_tensor_name}, view_meta);
      {unwrap_tensor_args_str}
      {return_type} reference_tensor_output;
      {{
        at::AutoDispatchSkipFunctionalize guard;
        {meta_conversion_str}
        reference_tensor_output = at::_ops::{api_name}::call({', '.join(meta_call_args)});
      }}
      // See  Note [Propagating strides in the functionalization pass]
      at::functionalization::impl::set_sizes_strides_offset({view_tensor_name}, reference_tensor_output);
      return {view_tensor_name};
"""

    else:
        return f"""
      {unwrap_tensor_args_str}
      {return_type} tmp_output;
      {return_type} reference_tensor_output;
      {{
        at::AutoDispatchSkipFunctionalize guard;
        {meta_conversion_str}
        reference_tensor_output = at::_ops::{api_name}::call({', '.join(meta_call_args)});
        tmp_output = at::_ops::{api_name}::redispatch({', '.join(view_redispatch_args)});
        // I'm fusing the [alias removal], [mutation removal], [add views back] passes together.
        // Later, we'll want to turn them into separate passes (since e.g. vulkan only cares about alias removal).
      }}
      at::functionalization::ViewMeta view_meta = at::functionalization::ViewMeta(
        {forward_lambda.decl()} {{
          return {forward_lambda.inner_call()}
        }},
        {reverse_lambda.decl()} {{
          return {reverse_lambda.inner_call()}
        }}
      );
      auto out = at::functionalization::impl::create_functional_tensor_with_view_meta(tmp_output, {view_tensor_name}, view_meta);
      // See  Note [Propagating strides in the functionalization pass]
      at::functionalization::impl::set_sizes_strides_offset(out, reference_tensor_output);
      return out;
"""
