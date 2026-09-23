def emit_inplace_functionalization_body(
        f: NativeFunction,
        functional_op: Optional[NativeFunction]
) -> str:
    # mutation case
    assert(modifies_arguments(f))

    dispatcher_sig = DispatcherSignature.from_schema(f.func)

    keyset = 'dispatchKeySet & c10::after_func_keyset'
    return_type = dispatcher_sig.returns_type().remove_const_ref().cpp_type()

    unwrap_tensor_args_str, unwrapped_args_ctx = unwrap_tensor_args(dispatcher_sig)

    maybe_return = '' if len(f.func.returns) == 0 else 'return '
    sync_tensor_args = '\n      '.join(mapMaybe(
        lambda arg: f'at::functionalization::impl::sync({arg.name});'
                    if arg.type.is_tensor_like() else None,
        f.func.arguments.flat_all))

    # Note [functionalizating copy_() and not preserving strides]
    # copy_() can't be functionalized, since there doesn't exist an out-of-place variant.
    # We could add one, but that would be sub-optimal for functorch: copy() would need to allocate a fresh tensor.
    # This may seem like a large hack for one optimization, but copy_() is one of the most common inplace operators.
    # Instead, we can replace `self.copy_(src)` with `src.to(self).expand_as(self)`.
    # This maintains the exact same semantics, EXCEPT that we don't preserve the strides from `self`.
    # This seems like a reasonable tradeoff, for a few reasons:
    # - mutation removal is only used by functorch, and not by Vulkan or XLA. Functorch already doesn't preserve strides.
    # - There are actually a few other places where the functionalization pass currently doesn't support strides:
    #   calls to slice/diagonal_scatter don't currently preserve the strides of their inputs (but maybe we should fix this).
    if str(f.func.name) == 'copy_':
        exprs = [keyset] + [a.name for a in unwrapped_args_ctx]
        functional_call_str = f"""\
            auto tmp_intermediate = at::_ops::to_other::redispatch({keyset}, src_, self_, non_blocking, false, c10::nullopt);
            tmp_output = at::_ops::expand_as::redispatch({keyset}, tmp_intermediate, self_);"""
    elif functional_op is None:
        # We can't functionalize this inplace op, since we don't know what the corresponding functional op is.
        inplace_exprs = [keyset] + [e.expr for e in translate(unwrapped_args_ctx, dispatcher_sig.arguments(), method=False)]
        warn_str = "Note: the functionalization pass encountered an operator ({}) that it could not functionalize, \
because it couldn't find an out-of-place equivalent of the operator to call. \
Instead, it's calling the inplace/view operator directly. \
If this causes problems in your program, consider upstreaming the out-of-place op to PyTorch.".format(str(f.func.name))

        return f"""
      if (c10::impl::tls_local_dispatch_key_set().included_.has(c10::DispatchKey::Functionalize)) {{
          TORCH_WARN("{warn_str}");
      }}
      {sync_tensor_args}
      {unwrap_tensor_args_str}
      at::AutoDispatchSkipFunctionalize guard;
      // Redispatch as normally otherwise, since XLA has its own lowerings for special inplace ops.
      {maybe_return}at::_ops::{f.func.name.unambiguous_name()}::redispatch({', '.join(inplace_exprs)});
"""
    else:
        # call the out-of-place variant of the op
        functional_sig = DispatcherSignature.from_schema(functional_op.func)
        functional_exprs = [keyset] + [e.expr for e in translate(unwrapped_args_ctx, functional_sig.arguments(), method=False)]
        functional_call_str = \
            f"tmp_output = at::_ops::{functional_op.func.name.unambiguous_name()}::redispatch({', '.join(functional_exprs)});"

    mutable_input_post_processing = '\n'.join([
        f"""
      auto {a.name}_functional = at::functionalization::impl::unsafeGetFunctionalWrapper({a.name});
      {a.name}_functional->replace_(tmp_output);
      {a.name}_functional->commit_update();"""
        for a in f.func.arguments.flat_non_out
        if a.annotation and a.annotation.is_write and a.type.is_tensor_like()])

    return f"""
      {sync_tensor_args}
      {unwrap_tensor_args_str}
      {return_type} tmp_output;
      {{
          at::AutoDispatchSkipFunctionalize guard;
          // The functionalization pass explicitly doesn't pass out= parameters to the redispatch
          {functional_call_str}
      }}
      {mutable_input_post_processing}
      {return_str(f)};"""
