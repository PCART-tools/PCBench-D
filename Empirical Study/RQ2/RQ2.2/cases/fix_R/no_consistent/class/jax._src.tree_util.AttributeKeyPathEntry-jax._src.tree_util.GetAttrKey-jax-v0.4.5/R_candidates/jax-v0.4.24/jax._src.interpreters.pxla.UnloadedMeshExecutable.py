@dataclasses.dataclass
class UnloadedMeshExecutable:
  xla_executable: Any
  device_assignment: xc.DeviceList | Sequence[xc.Device]  # type: ignore
  backend: xb.XlaBackend
  input_avals: Sequence[ShapedArray]
  input_shardings: Sequence[sharding_impls.XLACompatibleSharding]
  output_avals: Sequence[ShapedArray]
  output_shardings: Sequence[sharding_impls.XLACompatibleSharding]
  committed: bool
  are_out_shardings_from_xla: Sequence[bool]
  name: str
  unordered_effects: list[core.Effect]
  ordered_effects: list[core.Effect]
  keepalive: Sequence[Any]
  host_callbacks: Sequence[Any]
  kept_var_idx: set[int]
  auto_spmd_lowering: bool
  in_layouts: Sequence[SpecifiedLayout | None]
  out_layouts: Sequence[SpecifiedLayout | None]
  all_args_info: AllArgsInfo | None

  def build_unsafe_call(self):
    if xla_extension_version >= 229:
      handle_args = InputsHandler(self.input_shardings)
    else:
      input_indices = _get_input_indices(self.input_avals, self.input_shardings,
                                         self.device_assignment)
      handle_args = InputsHandler(
          self.input_shardings, self.xla_executable.local_devices(), input_indices)
    handle_outs = global_avals_to_results_handler(
        self.output_avals, self.output_shardings, self.committed,
        self.are_out_shardings_from_xla)  # type: ignore  # arg-type

    unsafe_call = ExecuteReplicated(  # type: ignore  # assignment
        self.xla_executable, self.name, self.backend, handle_args,
        handle_outs, self.unordered_effects, self.ordered_effects, self.keepalive,
        bool(self.host_callbacks), self.kept_var_idx)
    return unsafe_call

  def load(self) -> MeshExecutable:
    return MeshExecutable(self.xla_executable, self.build_unsafe_call,
                          self.input_avals,
                          self.input_shardings, self.output_shardings,
                          self.auto_spmd_lowering, self.kept_var_idx,
                          self.in_layouts, self.out_layouts,
                          self.all_args_info, self)

  # May return a MeshExecutable in the compile_replicated case.
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
    allow_prop_to_outputs = tuple(is_unspecified(o) for o in out_shardings)

    mesh = None
    if auto_spmd_lowering:
      for i in it.chain.from_iterable([in_shardings, out_shardings]):
        if is_auto(i):
          mesh = i.mesh  # type: ignore
          break

    xla_executable, compile_options = _cached_compilation(
        hlo, name, mesh, spmd_lowering,
        tuple_args, auto_spmd_lowering, allow_prop_to_outputs,
        tuple(host_callbacks), backend, da, pmap_nreps,
        compiler_options_keys, compiler_options_values)

    if hasattr(backend, "compile_replicated"):
      semantics_in_shardings = SemanticallyEqualShardings(in_shardings)  # type: ignore
      semantics_out_shardings = SemanticallyEqualShardings(out_shardings)  # type: ignore
      return _compile_replicated_mesh_executable_from_hlo(
          hlo, name, tuple(global_in_avals), tuple(global_out_avals),
          semantics_in_shardings, semantics_out_shardings, auto_spmd_lowering,
          compile_options, tuple(host_callbacks), bool(unordered_effects),
          tuple(ordered_effects), tuple(kept_var_idx), backend, da, committed,
          pmap_nreps)

    if auto_spmd_lowering:
      assert mesh is not None
      in_shardings_xla, out_shardings_xla = _get_mesh_pspec_shardings_from_executable(
          xla_executable, mesh)
      in_shardings = [x if is_auto(i) else getattr(i, '_original_sharding', i)  # type: ignore
                      for x, i in safe_zip(in_shardings_xla, in_shardings)]
      out_shardings_tuple = [
          (x, True) if is_auto(o) else (o, False)
          for x, o in safe_zip(out_shardings_xla, out_shardings)
      ]
      out_shardings, are_out_shardings_from_xla = unzip2(out_shardings_tuple)
    else:
      if pmap_nreps == 1:
        assert mesh is None
        # TODO(yashkatariya): Make da directly usable in the downstream code
        # without tuple conversion.
        out_shardings, are_out_shardings_from_xla = _get_shardings_from_executable(
            xla_executable, out_shardings, tuple(da), global_out_avals,
            len(ordered_effects), all_default_mem_kind)
      else:
        in_shardings, out_shardings, committed, da = _get_metadata_jit_pmap(
            xla_executable.local_devices(), len(in_shardings), len(out_shardings))
        are_out_shardings_from_xla = (False,) * len(global_out_avals)

    if xla_extension_version >= 217:
      in_layouts, out_layouts = _get_layouts_from_executable(
          xla_executable, in_layouts, out_layouts, len(ordered_effects))
    else:
      assert all(i is None for i in in_layouts)
      assert all(o is None for o in out_layouts)

    out_shardings, are_out_shardings_from_xla = maybe_get_orig_out_sharding(
        in_shardings, out_shardings, are_out_shardings_from_xla,
        global_in_avals, global_out_avals)

    out_shardings, are_out_shardings_from_xla = finalize_out_shardings(
        out_shardings, are_out_shardings_from_xla, da)

    return UnloadedMeshExecutable(
        xla_executable=xla_executable,
        device_assignment=da,  # type: ignore
        backend=backend,
        input_avals=global_in_avals,
        input_shardings=in_shardings,  # type: ignore
        output_avals=global_out_avals,
        output_shardings=out_shardings,  # type: ignore # arg-type
        committed=committed,
        are_out_shardings_from_xla=are_out_shardings_from_xla,
        name=name,
        unordered_effects=unordered_effects,
        ordered_effects=ordered_effects,
        keepalive=keepalive,
        host_callbacks=host_callbacks,
        kept_var_idx=kept_var_idx,
        auto_spmd_lowering=auto_spmd_lowering,
        in_layouts=in_layouts,  # type: ignore
        out_layouts=out_layouts,  # type: ignore
        all_args_info=all_args_info).load()  # type: ignore
