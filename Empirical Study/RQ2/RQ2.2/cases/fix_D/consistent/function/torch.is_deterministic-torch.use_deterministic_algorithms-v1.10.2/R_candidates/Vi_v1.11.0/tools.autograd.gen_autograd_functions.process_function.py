def process_function(info: DifferentiabilityInfo, template: CodeTemplate) -> str:
    saved_variables: List[str] = []
    release_variables: List[str] = []
    saved_list_sizes: List[str] = []
    unpack: List[str] = []
    asserts: List[str] = []
    compute_index_ranges: List[str] = []
    getter_definitions: List[str] = []
    py_getsetdef_structs: List[str] = []

    for arg in info.args_with_derivatives:
        if arg.type == 'at::TensorList' or arg.type == 'const c10::List<c10::optional<at::Tensor>> &':
            size = f'{arg.name}_size_'
            saved_list_sizes.append(f'size_t {arg.name}_size_;')
        else:
            size = '1'
        compute_index_ranges.append(f'auto {arg.name}_ix = gen.range({size});')

    def save_var(var: SavedAttribute, is_output: bool) -> None:
        name = var.nctype.name
        type = var.nctype.type
        should_append_getsetdef = True
        should_append_raw_getsetdef = False

        if type == BaseCType(tensorT) or type == OptionalCType(BaseCType(tensorT)) or \
                type == MutRefCType(OptionalCType(BaseCType(tensorT))) or \
                (type == BaseCType(scalarT) and is_output):
            saved_variables.append(f'SavedVariable {name}_;')
            release_variables.append(f'{name}_.reset_data();')
            ptr = 'shared_from_this()' if is_output else ''
            unpack.append(f'auto {name} = {name}_.unpack({ptr});')
            getter_definitions.append(GETTER_DEFINITION_SAVEDVAR.substitute(
                op=info.op, name=name, body=GETTER_BODY_SAVEDVAR))
            getter_definitions.append(GETTER_DEFINITION_RAW_SAVEDVAR.substitute(
                op=info.op, name=name, body=GETTER_BODY_RAW_SAVEDVAR))
            should_append_raw_getsetdef = True
        elif type == BaseCType(tensorListT):
            saved_variables.append(f'std::vector<SavedVariable> {name}_;')
            saved_variables.append(f'bool {name}_released_ = false;')
            # Just clear() is sufficient, we don't need to loop and clear each variable.
            # Because the SavedVariable owns a tensor and a grad_fn, removing the SavedVariable makes them go away as well.
            release_variables.append(f'{name}_.clear();')
            release_variables.append(f'{name}_released_ = true;')
            unpack.append(f'auto {name} = unpack_list({name}_);')
            asserts.append(f'TORCH_CHECK(!{name}_released_, ERR_BACKWARD_TWICE);')
            getter_definitions.append(GETTER_DEFINITION_VEC_SAVEDVAR.substitute(
                op=info.op, name=name, body=GETTER_BODY_VEC_SAVEDVAR))
            getter_definitions.append(GETTER_DEFINITION_RAW_VEC_SAVEDVAR.substitute(
                op=info.op, name=name, body=GETTER_BODY_RAW_VEC_SAVEDVAR))
            should_append_raw_getsetdef = True
        elif type == ListCType(OptionalCType(BaseCType(tensorT))):
            saved_variables.append(f'std::vector<SavedVariable> {name}_;')
            saved_variables.append(f'bool {name}_released_ = false;')
            # Just clear() is sufficient, we don't need to loop and clear each variable.
            # Because the SavedVariable owns a tensor and a grad_fn, removing the SavedVariable makes them go away as well.
            release_variables.append(f'{name}_.clear();')
            release_variables.append(f'{name}_released_ = true;')
            unpack.append(f'auto {name} = unpack_opt_list({name}_);')
            asserts.append(f'TORCH_CHECK(!{name}_released_, ERR_BACKWARD_TWICE);')
            getter_definitions.append(GETTER_DEFINITION_VEC_SAVEDVAR.substitute(
                op=info.op, name=name, body=GETTER_BODY_VEC_SAVEDVAR))
            getter_definitions.append(GETTER_DEFINITION_RAW_VEC_SAVEDVAR.substitute(
                op=info.op, name=name, body=GETTER_BODY_RAW_VEC_SAVEDVAR))
            should_append_raw_getsetdef = True
        elif type == BaseCType(intArrayRefT):
            saved_variables.append(f'std::vector<int64_t> {name};')
            getter_definitions.append(GETTER_DEFINITION.substitute(
                op=info.op, name=name, body=GETTER_BODY_ARRAYREF_LONG))
        elif type == OptionalCType(BaseCType(intArrayRefT)):
            saved_variables.append(f'c10::OptionalArray<int64_t> {name};')
            getter_definitions.append(GETTER_DEFINITION_OPT_ARRAYREF.substitute(
                op=info.op, name=name, body=GETTER_BODY_ARRAYREF_LONG))
        elif type == OptionalCType(ArrayRefCType(BaseCType(doubleT))):
            saved_variables.append(f'c10::OptionalArray<double> {name};')
            getter_definitions.append(GETTER_DEFINITION_OPT_ARRAYREF.substitute(
                op=info.op, name=name, body=GETTER_BODY_ARRAYREF_DOUBLE))
        elif type == BaseCType(longT):
            saved_variables.append(f'{type.cpp_type()} {name} = 0;')
            getter_definitions.append(GETTER_DEFINITION.substitute(
                op=info.op, name=name, body=GETTER_BODY_INT64_T))
        elif type == BaseCType(stringT):
            saved_variables.append(f'std::string {name};')
            getter_definitions.append(GETTER_DEFINITION.substitute(
                op=info.op, name=name, body=GETTER_BODY_STRING))
        elif type == OptionalCType(BaseCType(stringT)):
            saved_variables.append(f'c10::optional<std::string> {name};')
            getter_definitions.append(GETTER_DEFINITION_OPT.substitute(
                op=info.op, name=name, body=GETTER_BODY_STRING))
        else:
            saved_variables.append(f'{type.cpp_type()} {name};')

            if type in MISC_GETTER_DEFS:
                getter_def, body = MISC_GETTER_DEFS[type]
                getter_definitions.append(getter_def.substitute(op=info.op, name=name, body=body))
            else:
                # Types we don't expose python bindings to yet:
                #   TypeAndSize, at::ScalarType, TensorOptions, TensorGeometry,
                #   std::vector<std::vector<int64_t>>, std::vector<at::ScalarType>
                should_append_getsetdef = False

        if should_append_getsetdef:
            py_getsetdef_structs.append(PY_GETSETDEF_STRUCT.substitute(op=info.op, name=name))
        if should_append_raw_getsetdef:
            py_getsetdef_structs.append(PY_RAW_GETSETDEF_STRUCT.substitute(op=info.op, name=name))

    for var in info.all_saved_inputs:
        save_var(var, is_output=False)
    for var in info.all_saved_outputs:
        save_var(var, is_output=True)

    # lock the mutex when we release variables and in Node::apply to protect thread safety
    # see Note [Thread Safety on Autograd Node]
    if len(release_variables) > 0:
        thread_lock = 'std::lock_guard<std::mutex> lock(mutex_);'
    else:
        thread_lock = ''

    if uses_retain_variables(info):
        will_release_variables = WILL_RELEASE_VARIABLES.substitute()
    else:
        will_release_variables = ''

    body: List[str] = []

    if uses_single_grad(info):
        body.append('const auto& grad = grads[0];')
    else:
        # Generate aliases for gradients named for returned values.
        body.extend(
            f'const auto& {name} = grads[{info.available_named_gradients.index(name)}];'
            for name in info.used_named_gradients)

    def emit_derivative(
        derivative: Derivative,
        args_with_derivatives: Sequence[Binding],
    ) -> Tuple[bool, str]:
        formula = derivative.formula
        var_names = derivative.var_names
        if len(var_names) == 1:
            checks_any_grad_defined = False
            if 'not_implemented' not in formula:
                matching_args = [
                    arg for arg in args_with_derivatives
                    if arg.name == var_names[0]]
                if len(matching_args) == 1:
                    # We can add undefined grad support if the input variable is a Tensor
                    arg = matching_args[0]
                    if isinstance(arg.argument, Argument) and str(arg.argument.type) in ('Tensor', 'Tensor?'):
                        formula = 'any_grad_defined ? (' + formula + ') : Tensor()'
                        checks_any_grad_defined = True
            return (checks_any_grad_defined,
                    DERIVATIVE_SINGLE.substitute(name=var_names[0], derivative=formula))
        else:
            if 'grad_input_mask' in formula:
                masks = [f'should_compute_output({{ {n}_ix }}),' for n in var_names]
                grad_input_mask = GRAD_INPUT_MASK.substitute(masks=masks, n=len(var_names))
            else:
                grad_input_mask = ''
            idx_ranges = ', '.join(f'{n}_ix' for n in var_names)
            copy_ranges: List[str] = []
            for i, n in enumerate(var_names):
                copy_ranges.append(DERIVATIVE_MULTI_COPY_RANGE.substitute(name=n, i=i))
            return False, DERIVATIVE_MULTI.substitute(
                idx_ranges=idx_ranges, copy_ranges=copy_ranges,
                derivative=formula,
                grad_input_mask=grad_input_mask)

    body.extend(unpack)
    need_any_grad_defined_var = False
    for derivative in info.derivatives:
        checks_any_grad_defined, derivative_text = emit_derivative(derivative, info.args_with_derivatives)
        body.append(derivative_text)
        need_any_grad_defined_var |= checks_any_grad_defined
    # Since single-output derivative formulas need to check if grads are
    # defined, only perform the check once, before all the formulas
    if need_any_grad_defined_var:
        body.insert(-len(info.derivatives),
                    'bool any_grad_defined = any_variable_defined(grads);')

    if info.name in UNTRACEABLE_FUNCTIONS:
        superclass = 'Node'
    else:
        superclass = 'TraceableFunction'

    all_getsetdef_structs = ",\n".join(py_getsetdef_structs) + "," if len(py_getsetdef_structs) != 0 else ""
    all_getter_definitions = "\n".join(getter_definitions)

    return template.substitute(
        op=info.op,
        compute_index_ranges=compute_index_ranges,
        saved_variables=saved_variables,
        release_variables=release_variables,
        saved_list_sizes=saved_list_sizes,
        asserts=asserts,
        thread_lock=thread_lock,
        will_release_variables=will_release_variables,
        body=body,
        superclass=superclass,
        all_getter_definitions=all_getter_definitions,
        all_getsetdef_structs=all_getsetdef_structs
    )
