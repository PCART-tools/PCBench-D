def lower_jaxpr_to_fun(
    ctx: ModuleContext,
    name: str,
    jaxpr: core.ClosedJaxpr,
    effects: Sequence[core.Effect],
    *,
    create_tokens: bool = False,
    public: bool = False,
    replace_tokens_with_dummy: bool = False,
    replicated_args: Optional[Sequence[bool]] = None,
    arg_shardings: Optional[Sequence[Optional[xc.OpSharding]]] = None,
    result_shardings: Optional[Sequence[Optional[xc.OpSharding]]] = None,
    use_sharding_annotations: bool = True,
    input_output_aliases: Optional[Sequence[Optional[int]]] = None,
    num_output_tokens: int = 0,
    api_name: str = 'jit',
    arg_names: Optional[Sequence[str]] = None,
    result_names: Optional[Sequence[str]] = None,
) -> func_dialect.FuncOp:
  """Lowers jaxpr and its callees to an IR function.

  Assumes that an MLIR context, location, and insertion point are set.

  Args:
    ctx: the lowering context.
    name: the function name. The name will be uniquified by the symbol table,
      so it is ok to use the same name multiple times.
    jaxpr: the jaxpr to lower.
    effects: a sequence of `core.Effect`s corresponding to an ordering of tokens
      that will be created in or used by the lowered function.
    create_tokens: if true, the HLO will create tokens and ignore dummy input tokens.
    public: if true, the function's visibility is set to "public".
    replace_tokens_with_dummy: if true, token arguments/return values are
      replaced with bool arrays of size [0].
    replicated_args: if present, annotates arguments as replicated.
    arg_shardings: sharding annotations for each argument (optional).
    result_shardings: sharding annotations for each argument (optional).
    use_sharding_annotations: if True, use "mhlo.sharding" annotations on
      parameters and return values to express sharding. If False, use
      hlo.custom_call operators with sharding annotations.
      TODO(b/228598865): remove this option when "mhlo.sharding" annotations are
      propagated on non-entry functions during MLIR->HLO conversion.
    input_output_aliases: optional sequence that maps argument numbers to the
      corresponding output that should alias them.
    api_name: The name of the higher level primitive which should show up in the
      name stack.
  Returns the name of the function.
  """
  def aval_to_types(aval):
    if replace_tokens_with_dummy and aval is core.abstract_token:
      aval = core.ShapedArray((), np.dtype(np.bool_))
    return aval_to_ir_types(aval)

  num_dim_vars = len(ctx.dim_vars)
  dim_var_types = map(aval_to_types, [core.ShapedArray((), dtypes.canonicalize_dtype(np.int64))] * num_dim_vars)

  # Function inputs: *dim_var_values, *tokens, *actual_inputs
  input_types = map(aval_to_types, jaxpr.in_avals)
  output_types = map(aval_to_types, jaxpr.out_avals)
  num_tokens = len(effects)

  if create_tokens:
    # If we create the tokens they won't be inputs to the MLIR function.
    token_types = [dummy_token_type() for _ in effects]
    output_token_types = [dummy_token_type() for _ in range(num_output_tokens)]
  else:
    # If we aren't creating tokens they will be the initial inputs to the
    # MLIR function.
    output_token_types = []
    num_tokens = len(effects)
    token_types = [token_type() for _ in effects]
  input_types = [*dim_var_types, *token_types, *input_types]
  output_types = [*output_token_types, *token_types, *output_types]
  if input_output_aliases is not None:
    token_input_output_aliases = [None] * (num_dim_vars + num_tokens)
    input_output_aliases = [*token_input_output_aliases, *input_output_aliases]
    # Update the existing aliases to account for the new output values
    input_output_aliases = [None if a is None
                            else a + num_output_tokens + num_tokens
                            for a in input_output_aliases]
  if arg_shardings is not None:
    token_shardings = [None] * (num_dim_vars + num_tokens)
    arg_shardings = [*token_shardings, *arg_shardings]
  if result_shardings is not None:
    token_shardings = [None] * (num_tokens + num_output_tokens)
    result_shardings = [*token_shardings, *result_shardings]
  if replicated_args is not None:
    token_replicated_args = [False] * (num_dim_vars + num_tokens)
    replicated_args = [*token_replicated_args, *replicated_args]
  flat_input_types = util.flatten(input_types)
  flat_output_types = util.flatten(output_types)
  ftype = ir.FunctionType.get(flat_input_types, flat_output_types)
  func_op = func_dialect.FuncOp(name, ftype, ip=ctx.ip)
  func_op.attributes["sym_visibility"] = ir.StringAttr.get(
      "public" if public else "private")
  ctx.symbol_table.insert(func_op)
  ir_arg_shardings = None
  if arg_shardings is not None:
    ir_arg_shardings = util.flatten(
        [[sharding] * len(types) for sharding, types
         in zip(arg_shardings, input_types)])
  ir_result_shardings = None
  if result_shardings is not None:
    ir_result_shardings = util.flatten(
        [[sharding] * len(types)
         for sharding, types in zip(result_shardings, output_types)])

  if (replicated_args is not None or ir_arg_shardings is not None
      or input_output_aliases is not None):
    arg_attrs: List[Dict[str, ir.Attribute]] = [
        {} for _ in range(len(flat_input_types))]

    if replicated_args is not None:
      replicated_ir_args = [[replicated] * len(types) for replicated, types
                            in zip(replicated_args, input_types)]
      for attrs, replicated in zip(arg_attrs, util.flatten(replicated_ir_args)):
        if replicated:
          attrs["mhlo.is_same_data_across_replicas"] = ir.UnitAttr.get()

    if use_sharding_annotations and ir_arg_shardings is not None:
      for attrs, sharding in zip(arg_attrs, ir_arg_shardings):
        if sharding is not None:
          attrs["mhlo.sharding"] = get_sharding_attr(sharding)

    if input_output_aliases is not None:
      output_ids = util.unflatten(list(range(len(flat_output_types))),
                                  map(len, output_types))
      aliases: List[Optional[int]] = []
      for types, alias in zip(input_types, input_output_aliases):
        if alias is None:
          aliases.extend([None] * len(types))
        else:
          aliases.extend(output_ids[alias])

      for attrs, alias in zip(arg_attrs, aliases):
        if alias is not None:
          attrs["tf.aliasing_output"] = i32_attr(alias)

    if config.jax_jit_pjit_api_merge and arg_names:
      named_arg_attrs = arg_attrs[num_dim_vars + num_tokens:]
      if len(named_arg_attrs) == len(arg_names):
        for attrs, name_ in zip(named_arg_attrs, arg_names):
          attrs['jax.arg_info'] = ir.StringAttr.get(name_)

    func_op.arg_attrs = ir.ArrayAttr.get(
        [ir.DictAttr.get(attrs) for attrs in arg_attrs])

  result_attrs: List[Dict[str, ir.Attribute]] = [
      {} for _ in range(len(flat_output_types))]

  if config.jax_jit_pjit_api_merge and result_names:
    named_result_attrs = result_attrs[num_tokens:]
    if len(named_result_attrs) == len(result_names):
      for attrs, name_ in zip(named_result_attrs, result_names):
        attrs['jax.result_info'] = ir.StringAttr.get(name_)

  if use_sharding_annotations and ir_result_shardings is not None:
    for attrs, sharding in zip(result_attrs, ir_result_shardings):
      if sharding is not None:
        attrs['mhlo.sharding'] = get_sharding_attr(sharding)

    # func_op.result_attrs = ir.ArrayAttr.get([
    #         ir.DictAttr.get(
    #         {} if sharding is None else
    #         {"mhlo.sharding": get_sharding_attr(sharding)}
    #     ) for sharding in ir_result_shardings
    # ])

  func_op.result_attrs = ir.ArrayAttr.get(
      [ir.DictAttr.get(attrs) for attrs in result_attrs])

  entry_block = func_op.add_entry_block()
  with ir.InsertionPoint(entry_block):
    flat_args = entry_block.arguments
    if not use_sharding_annotations and ir_arg_shardings is not None:
      flat_args = [a if s is None else wrap_with_sharding_op(a, s)
                   for a, s in zip(flat_args, ir_arg_shardings)]

    unflattened_args = util.unflatten(flat_args, map(len, input_types))
    # We separate out the dimension variable inputs, the token inputs and
    # the usual inputs. The dimension variables and token inputs
    # will be passed to `jaxpr_subcomp` separately from the `args`.
    dim_var_values, token_args, unflattened_args = util.split_list(unflattened_args, [num_dim_vars, num_tokens])
    if create_tokens:
      tokens_in = TokenSet.create(effects)
    else:
      tokens_in = TokenSet(zip(effects, token_args))
    args: List[List[ir.Value]] = []
    for aval, arg in zip(jaxpr.in_avals, unflattened_args):
      if replace_tokens_with_dummy and aval is core.abstract_token:
        args.append(hlo.CreateTokenOp().results)
      else:
        args.append(arg)
    callee_name_stack = ctx.name_stack.extend(util.wrap_name(name, api_name))
    out_vals, tokens_out = jaxpr_subcomp(ctx.replace(name_stack=callee_name_stack),
                                         jaxpr.jaxpr, tokens_in, map(ir_constants, jaxpr.consts),
                                         *args, dim_var_values=dim_var_values)
    outs = []
    if create_tokens:
      for _ in range(num_output_tokens):
        outs.append(dummy_token())
      for _ in effects:
        outs.append(dummy_token())
    else:
      for eff in effects:
        outs.append(tokens_out.get(eff))
    for aval, out in zip(jaxpr.out_avals, out_vals):
      if replace_tokens_with_dummy and aval is core.abstract_token:
        outs.append(ir_constants(np.zeros((), np.bool_)))
      else:
        outs.append(out)
    flat_outputs = util.flatten(outs)
    if not use_sharding_annotations and ir_result_shardings is not None:
      flat_outputs = [o if s is None else wrap_with_sharding_op(o, s)
                      for o, s in zip(flat_outputs, ir_result_shardings)]

    func_dialect.ReturnOp(flat_outputs)

  return func_op
