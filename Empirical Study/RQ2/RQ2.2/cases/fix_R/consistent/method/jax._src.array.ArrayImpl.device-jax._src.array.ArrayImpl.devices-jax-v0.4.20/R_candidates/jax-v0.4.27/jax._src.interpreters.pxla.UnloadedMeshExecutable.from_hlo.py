  @staticmethod
  def from_hlo(name: str,
               hlo: ir.Module,
               global_in_avals: Sequence[ShapedArray],
               global_out_avals: Sequence[ShapedArray],
               in_shardings: Sequence[sharding_impls.XLACompatibleSharding | AUTO],
               out_shardings: Sequence[(sharding_impls.XLACompatibleSharding | AUTO |
                                        UnspecifiedValue)],
               spmd_lowering: bool,
               tuple_args: bool,
               auto_spmd_lowering: bool,
               unordered_effects: list[core.Effect],
               ordered_effects: list[core.Effect],
               host_callbacks: list[Any],
               keepalive: Any,
               kept_var_idx: set[int],
               backend: xb.XlaBackend,
               device_assignment: xc.DeviceList | Sequence[xc.Device],  # type: ignore
               committed: bool,
               in_layouts: MaybeLayout,
               out_layouts: MaybeLayout,
               pmap_nreps: int = 1,
               mut: MutationData | None = None,
               shape_poly_state: mlir.ShapePolyLoweringState | None = None,
               all_default_mem_kind: bool = True,
               all_args_info: AllArgsInfo | None = None,
               compiler_options=None,
  ) -> MeshExecutable:
    if shape_poly_state is not None and shape_poly_state.uses_dim_vars:
      hlo = mlir.refine_polymorphic_shapes(hlo)
    compiler_options_keys = tuple(
        compiler_options.keys()) if compiler_options is not None else None
    compiler_options_values = tuple(
        compiler_options.values()) if compiler_options is not None else None
    if isinstance(device_assignment, xc.DeviceList):
      da = device_assignment
    else:
      da = _create_da_object(tuple(device_assignment))
    del device_assignment

    allow_prop_to_inputs = tuple(is_unspecified(i) or is_auto(i)
                                 for i in in_shardings)
    allow_prop_to_outputs = tuple(is_unspecified(o) or is_auto(o)
                                  for o in out_shardings)

    mesh = None
    if auto_spmd_lowering:
      for i in it.chain.from_iterable([in_shardings, out_shardings]):
        if is_auto(i):
          mesh = i.mesh  # type: ignore
          break

    xla_executable = _cached_compilation(
        hlo, name, mesh, spmd_lowering,
        tuple_args, auto_spmd_lowering, allow_prop_to_inputs,
        allow_prop_to_outputs, tuple(host_callbacks), backend, da, pmap_nreps,
        compiler_options_keys, compiler_options_values)

    if auto_spmd_lowering:
      assert mesh is not None
      in_shardings_xla, out_shardings_xla = _get_mesh_pspec_shardings_from_executable(
          xla_executable, mesh)
      in_shardings = [x if is_auto(i) else i
                      for x, i in safe_zip(in_shardings_xla, in_shardings)]
      out_shardings = [x if is_auto(o) else o
                       for x, o in safe_zip(out_shardings_xla, out_shardings)]
    else:
      if pmap_nreps == 1:
        assert mesh is None
        if xla_extension_version >= 241:
          in_shardings = _maybe_get_and_check_in_shardings(
              xla_executable, in_shardings, tuple(da), global_in_avals,
              len(ordered_effects))
        out_shardings = _maybe_get_and_check_out_shardings(
            xla_executable, out_shardings, tuple(da), global_out_avals,
            len(ordered_effects), all_default_mem_kind)
      else:
        in_shardings, out_shardings, committed, da = _get_metadata_jit_pmap(
            xla_executable.local_devices(), len(in_shardings), len(out_shardings))

    in_layouts, out_layouts = _get_layouts_from_executable(
        xla_executable, in_layouts, out_layouts, len(ordered_effects))

    out_shardings = maybe_recover_user_shardings(
        in_shardings, out_shardings, global_in_avals, global_out_avals)

    out_shardings = finalize_out_shardings(out_shardings, da)

    return UnloadedMeshExecutable(
        xla_executable=xla_executable,
        device_assignment=da,  # type: ignore
        backend=backend,
        input_avals=global_in_avals,
        input_shardings=in_shardings,  # type: ignore
        output_avals=global_out_avals,
        output_shardings=out_shardings,  # type: ignore # arg-type
        committed=committed,
        name=name,
        unordered_effects=unordered_effects,
        ordered_effects=ordered_effects,
        keepalive=keepalive,
        host_callbacks=host_callbacks,
        kept_var_idx=kept_var_idx,
        mut=mut,
        auto_spmd_lowering=auto_spmd_lowering,
        in_layouts=in_layouts,  # type: ignore
        out_layouts=out_layouts,  # type: ignore
        all_args_info=all_args_info).load()  # type: ignore
