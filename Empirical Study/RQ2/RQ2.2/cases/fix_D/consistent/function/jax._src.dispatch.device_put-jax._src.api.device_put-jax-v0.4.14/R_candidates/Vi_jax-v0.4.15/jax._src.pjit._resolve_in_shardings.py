def _resolve_in_shardings(
    args, pjit_in_shardings: Sequence[PjitSharding],
    out_shardings: Sequence[PjitSharding],
    pjit_mesh: Optional[pxla.Mesh]) -> Sequence[PjitSharding]:
  # If True, means that device or backend is set by the user on pjit and it
  # has the same semantics as device_put i.e. doesn't matter which device the
  # arg is on, reshard it to the device mentioned. So don't do any of the
  # checks and just return the pjit_in_shardings directly. `shard_args` will
  # handle the resharding.
  if pxla.check_device_backend_on_shardings(pjit_in_shardings):
    return pjit_in_shardings

  committed_arg_shardings = []
  for a in args:
    if hasattr(a, 'sharding'):
      arg_s = a.sharding
      # arg sharding can be None in case of ShapeDtypeStruct. jax.Array does
      # not allow None as the sharding.
      if arg_s is None:
        continue
      if not isinstance(arg_s, XLACompatibleSharding):
        raise ValueError(f'One of the argument to pjit got sharding {arg_s} '
                         'which is not a subclass of XLACompatibleSharding.')
      # Don't consider PmapSharding inputs as committed. They will get resharded
      # unconditionally.
      if isinstance(arg_s, PmapSharding):
        continue
      if getattr(a, '_committed', True):
        committed_arg_shardings.append((arg_s, pxla.MismatchType.ARG_SHARDING, None))

  # Check if the device_assignment across inputs, outputs and arguments is the
  # same.
  pxla._get_and_check_device_assignment(
      it.chain(
          committed_arg_shardings,
          [(i, pxla.MismatchType.IN_SHARDING, None) for i in pjit_in_shardings],
          [(o, pxla.MismatchType.OUT_SHARDING, None) for o in out_shardings]),
      (None if pjit_mesh is None or pjit_mesh.empty else list(pjit_mesh.devices.flat)))

  resolved_in_shardings = []
  for arg, pjit_in_s in zip(args, pjit_in_shardings):
    # arg sharding can be None in case of ShapeDtypeStruct. jax.Array does
    # not allow None as the sharding.
    arg_s, committed = ((arg.sharding, getattr(arg, '_committed', True))
                        if hasattr(arg, 'sharding') and arg.sharding is not None
                        else (UNSPECIFIED, False))
    if is_unspecified(pjit_in_s):
      if is_unspecified(arg_s):
        resolved_in_shardings.append(arg_s)
      else:
        if committed:
          # If the arg has a PmapSharding, then reshard it unconditionally.
          if isinstance(arg_s, PmapSharding):
            resolved_in_shardings.append(UNSPECIFIED)
          else:
            resolved_in_shardings.append(to_gspmd_sharding(
                cast(XLACompatibleSharding, arg_s), arg.ndim))
        else:
          if dispatch.is_single_device_sharding(arg_s):
            resolved_in_shardings.append(UNSPECIFIED)
          else:
            raise NotImplementedError('Having uncommitted Array sharded on '
                                      'multiple devices is not supported.')
    else:
      if (isinstance(arg, np.ndarray) and
          not pjit_in_s.is_fully_replicated and  # type: ignore
          xb.process_count() > 1):
        raise ValueError(
            'Passing non-trivial shardings for numpy '
            'inputs is not allowed. To fix this error, either specify a '
            'replicated sharding explicitly or use '
            '`jax.experimental.multihost_utils.host_local_array_to_global_array(...)` '
            'to convert your host local numpy inputs to a jax.Array which you '
            'can pass to pjit. '
            'If the numpy input is the same on each process, then you can use '
            '`jax.make_array_from_callback(...) to create a `jax.Array` which '
            'you can pass to pjit. '
            'Please see the jax.Array migration guide for more information '
            'https://jax.readthedocs.io/en/latest/jax_array_migration.html#handling-of-host-local-inputs-to-pjit-like-batch-etc. '
            f'Got arg shape: {arg.shape}, arg value: {arg}')
      if not is_unspecified(arg_s):
        # jax.jit does not allow resharding across different memory kinds even
        # if the argument is uncommitted. Use jax.device_put for those cases,
        # either outside or inside jax.jit.
        if pjit_in_s.memory_kind != arg_s.memory_kind:  # type: ignore
          raise ValueError(
              'Memory kinds passed to jax.jit does not match memory kind on the'
              f' respective arg. Got pjit memory kind: {pjit_in_s.memory_kind}, '  # type: ignore
              f'arg memory kind: {arg_s.memory_kind} for '  # type: ignore
              f'arg shape: {shaped_abstractify(arg).str_short()}')
        if (committed and
            not isinstance(arg_s, PmapSharding) and
            not op_shardings.are_op_shardings_equal(
                pjit_in_s._to_xla_hlo_sharding(arg.ndim),  # type: ignore
                arg_s._to_xla_hlo_sharding(arg.ndim))):
          op =  getattr(pjit_in_s, '_original_sharding', pjit_in_s)
          raise ValueError('Sharding passed to pjit does not match the sharding '
                           'on the respective arg. '
                           f'Got pjit sharding: {op},\n'
                           f'arg sharding: {arg_s} for '
                           f'arg shape: {shaped_abstractify(arg).str_short()}')
      resolved_in_shardings.append(pjit_in_s)

  return tuple(resolved_in_shardings)
