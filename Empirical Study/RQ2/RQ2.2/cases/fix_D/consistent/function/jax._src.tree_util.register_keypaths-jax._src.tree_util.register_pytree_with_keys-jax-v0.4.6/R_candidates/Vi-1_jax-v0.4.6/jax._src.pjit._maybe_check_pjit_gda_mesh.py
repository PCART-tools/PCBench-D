def _maybe_check_pjit_gda_mesh(args, mesh):
  for x in args:
    if isinstance(x, GDA) and x.mesh != mesh:
      raise ValueError("Pjit's mesh and GDA's mesh should be equal. Got Pjit "
                       f"mesh: {mesh},\n GDA mesh: {x.mesh}")
