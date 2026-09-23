def gen_variable_type_func(
    fn: NativeFunctionWithDifferentiabilityInfo
) -> Dict[str, List[str]]:
    f = fn.func
    with native_function_manager(f):
        name = cpp.name(f.func)
        formals = gen_formals(f)

        if fn.info is None and not get_base_name(f) in RESET_GRAD_ACCUMULATOR \
                and not get_base_name(f) in DONT_REQUIRE_DERIVATIVE \
                and len(gen_differentiable_outputs(fn)) > 0 \
                and not cpp.name(f.func) in DONT_ENFORCE_SAME_TENSOR_IMPL_OR_STORAGE \
                and not type_wrapper_name(f) in DONT_ENFORCE_STORAGE_IMPL_USE_COUNT \
                and not type_wrapper_name(f) in DONT_ENFORCE_TENSOR_IMPL_USE_COUNT:
            # NOTE: [ Registering AutogradNotImplemented boxed kernel ]
            #
            # When there is no derivatives.yaml entry, we register a generic boxed
            # NotImplemented kernel to set grad_fn to be NotImplemented, so that forward
            # proceeds as usual but an error is properly produced on backward.
            # TODO: it would be nice to not have these special cases
            #
            # There are several cases where still let codegen handle it:
            # 1) ops that need to reset grad accumulator (we let codegen handle this case
            #     because) the list is (currently) only accessible in Python.
            # 2) User explicitly specifies DONT_REQUIRE_DERIVATIVE. This basically makes
            #    autograd a fallthrough with NDEBUG checks. This can be useful for when all
            #    outputs are integral.
            # 3) When there are no differentiable outputs. This is similar to (2).
            # 4) There are certain ops where we skip certain NDEBUG checks. this is similar
            #    to (1).
            type_definition = ""
            wrapper_registration = AUTOGRAD_NOT_IMPLEMENTED_REGISTRATION.substitute(
                unqual_operator_name_with_overload=f.func.name)
        else:
            type_definition = METHOD_DEFINITION.substitute(
                return_type=cpp.returns_type(f.func.returns).cpp_type(),
                type_wrapper_name=type_wrapper_name(f),
                type_definition_body=emit_body(fn),
                formals=formals,
            )
            wrapper_registration = gen_wrapper_registration(f)

    # See Note [Manual Backend kernels]
    assert (name in MANUAL_BACKEND) == f.manual_kernel_registration
    # If you want to register a kernel to Autograd, you must make the op abstract.
    # In other words, this op must have dispatch section in native_functions.yaml.
    if name in MANUAL_AUTOGRAD_AND_TRACER or (fn.info and fn.info.has_derivatives):
        msg = (f'There\'s a formula for {name}(or its functional variant) in derivatives.yaml. '
               f'It\'s required to add a dispatch section for it with explicit supported backends e.g CPU/CUDA '
               f'or CompositeExplicitAutograd in native_functions.yaml. Please see '
               f'https://github.com/pytorch/pytorch/tree/master/aten/src/ATen/native#choosing-the-right-dispatch-keyword '
               f'for instructions to choose the right dispatch keyword.')
        assert f.is_abstract, msg

    return {
        'type_derived_method_definitions': [type_definition],
        'wrapper_registrations': [wrapper_registration],
    }
