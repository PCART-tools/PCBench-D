def match_differentiability_info(
    native_functions: List[NativeFunction],
    differentiability_infos: Sequence[DifferentiabilityInfo],
) -> List[NativeFunctionWithDifferentiabilityInfo]:
    """Sets the "derivative" key on declarations to matching autograd function
    In-place functions will use the out-of-place derivative definition if there
    is no in-place specific derivative.
    """

    info_by_schema = {info.func.func: info for info in differentiability_infos}
    functional_info_by_signature = {
        info.func.func.signature(strip_default=True): info
        for info in differentiability_infos
        if info.func.func.kind() == SchemaKind.functional}

    def find_info(f: NativeFunction) -> Tuple[Optional[DifferentiabilityInfo], bool]:
        if f.func in info_by_schema:
            return info_by_schema[f.func], True

        # if there is no exact match look for the out-of-place signature.
        # i.e mul() for mul_() or mul_out()
        return functional_info_by_signature.get(f.func.signature(strip_default=True)), False

    result: List[NativeFunctionWithDifferentiabilityInfo] = []
    for f in native_functions:
        info, is_exact_match = find_info(f)

        # Currently, the '.strides()' to 'strides_or_error' replacement does not support
        # 'self' derivatives of an inplace function, so we must check for this case.
        if f.func.kind() == SchemaKind.inplace and (info is not None):
            for derivative in info.derivatives:
                if 'self' in derivative.var_names:
                    for saved_input in derivative.saved_inputs:
                        assert 'strides_or_error' not in saved_input.expr, (
                            "Calling '.strides()' in the 'self' derivative formula of an "
                            f"in-place function is not supported: {f.func}")

        # For functions that have a single def for out-of-place and inplace (like abs())
        if info and info.forward_derivatives:
            forward_derivatives = info.forward_derivatives

            if f.func.kind() == SchemaKind.inplace:
                # For inplace functions there is a little bit of work to do:
                #  1) Validate the formula and make sure the input that is modified in not used:
                #    - If there is a formula for the inplace variant of the function (is_exact_match == True) then
                #      we make sure that the original value of the input that is being modified inplace (self_p) is
                #      not used in the formula. Note that the formula can use "original_self_p" here and that would
                #      trigger a clone of the original input.
                #    - If we are re-using the out of place formula (is_exact_match == False) then we replace every
                #      occurrence of self_p and self_t by original_self_p and original_self_t. These will be
                #      populated by cloned version of the original input (either the clone done by the backward AD
                #      logic if self is also used in a backward formula or a special clone that we add).
                #  2) At this point, there cannot be a self_p in the formula.
                #  3) Change "result" into "self_p" as by design, in the inplace function codegen, the result is
                #     simply called self (as it is modified inplace).
                #  4) Update the required primals data in case it used to contain "result" but should now contain
                #     "self"
                #  5) If it is not an exact match, the user formula is not modifying the existing forward grad
                #     inplace as it should. So add some code that makes sure that we do so if the forward grad
                #     already exists.

                assert len(info.forward_derivatives) == 1  # Only single output inplace should exist
                fw_info = info.forward_derivatives[0]
                formula = fw_info.formula

                def replace_self_with_original_self(formula: str, postfix: str) -> str:
                    def repl(m: Match[str]) -> str:
                        return f'{m.group(1)}original_self{postfix}{m.group(2)}'
                    return re.sub(IDENT_REGEX.format(f'self{postfix}'), repl, formula)

                if re.search(IDENT_REGEX.format("self_p"), formula):
                    if is_exact_match:
                        # For manually defined formulas, don't allow the original value to be used
                        raise RuntimeError(f'The formula for "{f.func.name}" is using the original value of self '
                                           'that is being modified inplace. This would lead to wrong forward gradients. '
                                           'Please use "result" in the formula only.')
                    else:
                        # When the original formula is out of place, we save a clone of the primal
                        # value to be able to access this value if needed
                        # replace "self_p"/"self_t" from the formula by "original_self_p"/"original_self_t"
                        formula = replace_self_with_original_self(formula, "_p")
                        formula = replace_self_with_original_self(formula, "_t")

                # replace "result" from the formula by "self_p"
                def repl(m: Match[str]) -> str:
                    return f'{m.group(1)}self_p{m.group(2)}'
                formula = re.sub(IDENT_REGEX.format("result"), repl, formula)

                required_primals = fw_info.required_inputs_primal
                if re.search(IDENT_REGEX.format("self_p"), formula):
                    required_primals = required_primals + ("self",) if required_primals else ("self",)

                if not is_exact_match:
                    # Make sure that the forward grad is modified inplace when the original formula
                    # is out of place
                    formula = f"self_t_raw.defined() ? self_t_raw.copy_({formula}) : {formula}"

                required_original_self_value = bool(re.search(IDENT_REGEX.format("original_self_p"), formula))

                forward_derivatives = [ForwardDerivative(
                    formula=formula,
                    var_name="self",
                    var_type=fw_info.var_type,
                    required_inputs_fw_grad=fw_info.required_inputs_fw_grad,
                    required_inputs_primal=required_primals,
                    required_original_self_value=required_original_self_value,
                    is_reusing_outplace_formula=not is_exact_match), ]
        else:
            forward_derivatives = []

        result.append(NativeFunctionWithDifferentiabilityInfo(
            func=f,
            info=info,
            fw_derivatives=forward_derivatives
        ))

    return result
