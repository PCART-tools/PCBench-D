def gen_functionalization_registration(
    selector: SelectiveBuilder,
    f: NativeFunction,
    composite_implicit_autograd_index: BackendIndex
) -> Optional[str]:
    @with_native_function
    def emit_registration_helper(f: NativeFunction) -> Optional[str]:
        # Note: for now, this logic is meant to avoid registering functionalization kernels for mobile.
        # At some point, Vulkan we'll want to use functionalization and we'll need to change this.
        if not needs_functionalization(selector, f):
            return None
        if f.is_view_op and f.has_composite_implicit_autograd_kernel:
            metadata = composite_implicit_autograd_index.get_kernel(f)
            assert metadata is not None
            native_api_name = metadata.kernel
            sig = DispatcherSignature.from_schema(f.func)
            # Note [Composite view ops in the functionalization pass]
            # We don't need to worry about implemententing functionalization kernels for views with
            # CompositeImplicitAutograd kernels, because we can just decompose them into their base operators.
            # We can't just opt the entire Functionalization dispatch key into the composite keyset though,
            # because we don't want to decompose non-view ops that are composite, like `at::ones`.
            registration_str = f'static_cast<{sig.ptr_type()}>(at::native::{native_api_name})'
        else:
            registration_str = f'TORCH_FN(functionalization::{wrapper_name(f.func)})'

        return f'm.impl("{f.func.name}", {registration_str});'

    return emit_registration_helper(f)
