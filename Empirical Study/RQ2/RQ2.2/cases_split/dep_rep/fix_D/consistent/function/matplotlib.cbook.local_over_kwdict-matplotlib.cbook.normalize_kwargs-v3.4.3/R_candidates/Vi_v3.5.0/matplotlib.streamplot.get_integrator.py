@_api.deprecated("3.5")
def get_integrator(u, v, dmap, minlength, maxlength, integration_direction):
    xy_traj = _get_integrator(
        u, v, dmap, minlength, maxlength, integration_direction)
    return (None if xy_traj is None
            else ([], []) if not len(xy_traj)
            else [*zip(*xy_traj)])
