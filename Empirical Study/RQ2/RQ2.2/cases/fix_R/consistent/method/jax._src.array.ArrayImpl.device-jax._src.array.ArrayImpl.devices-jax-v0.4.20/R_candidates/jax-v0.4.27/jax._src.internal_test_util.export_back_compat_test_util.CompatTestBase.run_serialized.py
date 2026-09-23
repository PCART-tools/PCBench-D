  def run_serialized(self, data: CompatTestData,
                     polymorphic_shapes: Sequence[str] | None = None):
    args_specs = export.symbolic_args_specs(data.inputs, polymorphic_shapes)
    def ndarray_to_aval(a: np.ndarray) -> core.ShapedArray:
      return core.ShapedArray(a.shape, a.dtype)
    in_avals_tree = tree_util.tree_map(ndarray_to_aval, args_specs)
    # TODO: we ought to ensure that out_avals are polymorphic if need be. We
    # could either save the in/out_avals (but we need to first implement that
    # support in export), or we can just re-use them from the current
    # exported.
    out_avals_tree = tree_util.tree_map(ndarray_to_aval, data.expected_outputs)
    # in_tree must be for (args, kwargs)
    in_avals, in_tree = tree_util.tree_flatten((in_avals_tree, {}))
    out_avals, out_tree = tree_util.tree_flatten(out_avals_tree)
    def _get_vjp(_):
      assert False  # We do not have and do not need VJP

    exported = export.Exported(
        fun_name="run_serialized",
        in_tree=in_tree,
        in_avals=tuple(in_avals),
        out_tree=out_tree,
        out_avals=tuple(out_avals),
        in_shardings=(None,) * len(in_avals),
        out_shardings=(None,) * len(out_avals),
        lowering_platforms=(data.platform,),
        ordered_effects=(),
        unordered_effects=(),
        disabled_safety_checks=(),
        mlir_module_serialized=data.mlir_module_serialized,
        mlir_module_serialization_version=data.xla_call_module_version,
        nr_devices=data.nr_devices,
        module_kept_var_idx=tuple(range(len(in_avals))),
        uses_shape_polymorphism=any(not core.is_constant_shape(a.shape)
                                    for a in in_avals),
      _get_vjp=_get_vjp)

      # We use pjit in case there are shardings in the exported module.
    return pjit.pjit(export.call_exported(exported))(*data.inputs)
