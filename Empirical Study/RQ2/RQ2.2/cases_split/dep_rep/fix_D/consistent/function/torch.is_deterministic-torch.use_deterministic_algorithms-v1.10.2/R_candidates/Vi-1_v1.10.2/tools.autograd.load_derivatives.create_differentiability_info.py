def create_differentiability_info(
    defn: Dict[Any, Any],
    functions_by_signature: Dict[FunctionSchema, List[NativeFunction]],
    functions_by_schema: Dict[str, NativeFunction],
    op_counter: Counter[str],
) -> DifferentiabilityInfo:
    """Processes a single entry `defn` in derivatives.yaml"""

    def canonical_function(functions: Sequence[NativeFunction], name: str) -> NativeFunction:
        for f in functions:
            if cpp.name(f.func) == name:
                return f
        # some functions only have in-place variants
        assert name + '_' == cpp.name(functions[0].func)
        return functions[0]

    def split_names(raw_names: str) -> Tuple[str, ...]:
        """Given "foo, bar", return ["foo", "bar"]."""
        return tuple(x.strip() for x in raw_names.split(','))

    def check_grad_usage(defn_name: str, derivatives: Sequence[Derivative]) -> None:
        """
        Check for some subtle mistakes one might make when writing derivatives.
        These mistakes will compile, but will be latent until a function is
        used with double backwards.
        """

        uses_grad = False                   # true if any derivative uses "grad"
        num_grads_uses = 0                  # count of uses of "grads" or "grads[INDEX]"
        uses_named_grads = False            # true if any derivative uses "grad_{name}"
        used_grads_indices: List[int] = []  # which indices of grads are used
        for d in derivatives:
            formula = d.formula
            uses_grad = uses_grad or bool(re.findall(IDENT_REGEX.format('grad'), formula))
            num_grads_uses += len(re.findall(IDENT_REGEX.format('grads'), formula))
            uses_named_grads = uses_named_grads or bool(d.named_gradients)
            used_grads_indices.extend(used_gradient_indices(formula))
        # This is a basic sanity check: the number of places we see
        # "grads" should be no fewer than the number of indices we see
        # inside "grads". They may not be equal because we may use
        # "grads" without an index.
        assert num_grads_uses >= len(used_grads_indices)
        # Thus if the number is equal, every use of grads is also
        # indexed.
        only_used_grads_indices = num_grads_uses == len(used_grads_indices)

        if uses_grad and num_grads_uses > 0:
            raise RuntimeError(f"Derivative definition of {defn_name} in derivatives.yaml illegally "
                               "mixes use of 'grad' and 'grads'. Consider replacing "
                               "occurrences of 'grad' with 'grads[0]'")

        if only_used_grads_indices and set(used_grads_indices) == {0}:
            raise RuntimeError(f"Derivative definition of {defn_name} in derivatives.yaml solely "
                               "refers to 'grads[0]'.  If the first output is indeed the "
                               "only differentiable output, replace 'grads[0]' with 'grad'; "
                               "otherwise, there is a likely error in your derivatives "
                               "declaration.")

        if uses_named_grads and (uses_grad or num_grads_uses > 0):
            raise RuntimeError(
                f'Derivative definition of {defn_name} in derivatives.yaml illegally '
                'mixes use of "grad_RETURN_NAME" and "grad" or "grads[x]". Use '
                'only one method for identifying gradients.')


    @with_native_function
    def set_up_derivatives(f: NativeFunction) -> Tuple[
        Sequence[Derivative],
        Sequence[ForwardDerivative],
        Sequence[Binding],
        Sequence[str],
        Sequence[str],
    ]:
        # Set up the derivative information
        derivatives: List[Derivative] = []
        forward_derivatives: List[ForwardDerivative] = []
        non_differentiable_arg_names: List[str] = []
        args_with_derivatives_set: Set[str] = set()

        all_arg_names = [a.name for a in cpp_arguments(f)]

        # output_differentiability is captured from the enclosed
        # scope. Don't modify it.
        #
        # If it is not present, then no output is explicitly
        # undifferentiable.
        #
        # It may be present and shorter than the length of return
        # values. If that's the case, any return value that does not
        # have a corresponding entry is considered not differentiable.
        differentiability = output_differentiability or [True] * len(f.func.returns)
        # A return is available as a named gradient ...
        available_named_gradients = [
            f'grad_{ret.name}' for ret, differentiable in zip(f.func.returns, differentiability)
            # if it has not been explicitly made undifferentiable
            if differentiable
            # and if it has a name
            and ret.name is not None
            # and if its type is differentiable
            and ret.type.is_tensor_like()]

        for raw_names in sorted(defn.keys()):
            formula = defn[raw_names]
            names = split_names(raw_names)

            if is_forward_derivative_definition(all_arg_names, names):
                forward_derivatives.append(create_forward_derivative(f, formula, names))
            else:
                if formula.lower().strip() == 'non_differentiable':
                    non_differentiable_arg_names += names
                else:
                    derivative = create_derivative(f, formula, names,
                                                   available_named_gradients)
                    derivatives.append(derivative)
                    args_with_derivatives_set |= set(names)

        overlap = args_with_derivatives_set.intersection(non_differentiable_arg_names)
        if overlap:
            raise RuntimeError(f'derivatives definition for {defn} have overlapped non_differentiable '
                               f'and differentiable variables: {overlap}')

        # Next, let us determine the list of inputs in order.
        # TODO: do we need eagerly calculate and save it here? Can it be derived
        # from NativeFunction and `derivatives` on callsites instead?
        args_with_derivatives = [a for a in cpp_arguments(f) if a.name in args_with_derivatives_set]

        # Postprocess forward derivatives definitions now that we know the differentiable arguments
        forward_derivatives = postprocess_forward_derivatives(f, defn_name, all_arg_names, derivatives,
                                                              forward_derivatives, args_with_derivatives)

        # Test to see if the use of 'grads' makes sense.
        check_grad_usage(defn_name, derivatives)

        return (derivatives, forward_derivatives, args_with_derivatives,
                non_differentiable_arg_names, available_named_gradients)

    # NB: Removes 'name' from defn dictionary
    specification = defn.pop('name')
    defn_name, _ = split_name_params(specification)
    # NB: Removes 'output_differentiability' from defn dictionary
    #     `None` means all differentiable.
    output_differentiability = defn.pop('output_differentiability', None)
    output_differentiability_conditions = None
    if output_differentiability and any([isinstance(diff, str) for diff in output_differentiability]):
        if len(output_differentiability) != 1:
            raise RuntimeError(f'Not supported: for {specification},'
                               f'output_differentiability must either be '
                               f'List[bool] or a List[str] where each str is a '
                               f'condition. In the case where it is a condition, '
                               f'we only support single-output functions. '
                               f'Please file us an issue. ')
        output_differentiability_conditions = output_differentiability
        output_differentiability = [True]

    schema_function = functions_by_schema.get(specification)
    if not schema_function:
        avail = '\n'.join(k for k, v in functions_by_schema.items() if cpp.name(v.func) == defn_name)
        raise RuntimeError(f'could not find ATen function for schema: {specification} '
                           f'.  Available signatures:\n{avail}')

    # now map this to the legacy schema; this isn't technically necessary, but we'd need some logic here
    # to map in-place schemas to the out-of-place variants.
    # TODO: maybe the logic to handle the legacy schema is no longer necessary?
    signature = schema_function.func.signature()
    functions = functions_by_signature[signature]
    if len(functions) == 0:
        avail = '\n'.join(str(k) for k, v in functions_by_signature.items() if cpp.name(k) == defn_name)
        raise RuntimeError(f'could not find ATen function for legacy signature: {signature} '
                           f'corresponding to schema {specification}.  Please report a bug to PyTorch. '
                           f'Available signatures:\n{avail}')

    canonical = canonical_function(functions, defn_name)
    if 'grad_input_mask' in (a.name for a in cpp_arguments(canonical)):
        raise RuntimeError(f"Schema for {defn_name} has an argument named grad_input_mask, "
                           "but this name would be shadowed by our codegen. "
                           "Please use a different name in native_functions.yaml.")

    if 'result' in (a.name for a in cpp_arguments(canonical)):
        raise RuntimeError(f"Schema for {defn_name} has an argument named result, "
                           "but this is only allowed for outputs."
                           "Please use a different name in native_functions.yaml.")

    (derivatives, forward_derivatives, args_with_derivatives,
     non_differentiable_arg_names, available_named_gradients) = set_up_derivatives(canonical)

    used_named_gradients: Set[str] = set()
    for d in derivatives:
        used_named_gradients |= d.named_gradients

    # only assign an op name if we are actually going to calculate a derivative
    op = None
    if args_with_derivatives:
        op_prefix = _create_op_prefix(defn_name)
        op = f'{op_prefix}{op_counter[op_prefix]}'
        op_counter[op_prefix] += 1

    return DifferentiabilityInfo(
        name=defn_name,
        func=canonical,
        op=op,
        derivatives=derivatives,
        forward_derivatives=forward_derivatives,
        all_saved_inputs=dedup_vars([v for d in derivatives for v in d.saved_inputs]),
        all_saved_outputs=dedup_vars([v for d in derivatives for v in d.saved_outputs]),
        available_named_gradients=available_named_gradients,
        used_named_gradients=used_named_gradients,
        args_with_derivatives=args_with_derivatives,
        non_differentiable_arg_names=non_differentiable_arg_names,
        output_differentiability=output_differentiability,
        output_differentiability_conditions=output_differentiability_conditions,
    )
