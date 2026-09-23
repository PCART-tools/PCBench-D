@with_native_function
def process_function(f: NativeFunction) -> Optional[str]:
    name = cpp.name(f.func)
    has_tensor_options = python.has_tensor_options(f)
    is_factory = has_tensor_options or name.endswith("_like")

    if Variant.function not in f.variants or not is_factory:
        return None

    sig = CppSignatureGroup.from_native_function(f, method=False).signature
    formals: List[str] = []
    exprs: List[str] = []
    requires_grad = 'false'
    for arg in sig.arguments():
        qualified_type = fully_qualified_type(arg.type)
        if arg.default:
            formals.append(f'{qualified_type} {arg.name} = {arg.default}')
        else:
            formals.append(f'{qualified_type} {arg.name}')

        if isinstance(arg.argument, TensorOptionsArguments):
            # note: we remove the requires_grad setting from the TensorOptions because
            # it is ignored anyways (and we actually have an assertion that it isn't set
            # which would fail otherwise). We handle requires_grad explicitly here
            # instead of passing it through to the kernel.
            exprs.append(f'at::TensorOptions({arg.name}).requires_grad(c10::nullopt)')
            # Manually set the requires_grad bit on the result tensor.
            requires_grad = f'{arg.name}.requires_grad()'
        else:
            exprs.append(arg.name)

    return f"""\
inline at::Tensor {name}({', '.join(formals)}) {{
  at::AutoDispatchBelowADInplaceOrView guard;
  return autograd::make_variable(at::{name}({', '.join(exprs)}), /*requires_grad=*/{requires_grad});
}}
"""
