def get_integrator(u, v, dmap, minlength, maxlength, integration_direction):

    # rescale velocity onto grid-coordinates for integrations.
    u, v = dmap.data2grid(u, v)

    # speed (path length) will be in axes-coordinates
    u_ax = u / (dmap.grid.nx - 1)
    v_ax = v / (dmap.grid.ny - 1)
    speed = np.ma.sqrt(u_ax ** 2 + v_ax ** 2)

    def forward_time(xi, yi):
        if not dmap.grid.within_grid(xi, yi):
            raise OutOfBounds
        ds_dt = interpgrid(speed, xi, yi)
        if ds_dt == 0:
            raise TerminateTrajectory()
        dt_ds = 1. / ds_dt
        ui = interpgrid(u, xi, yi)
        vi = interpgrid(v, xi, yi)
        return ui * dt_ds, vi * dt_ds

    def backward_time(xi, yi):
        dxi, dyi = forward_time(xi, yi)
        return -dxi, -dyi

    def integrate(x0, y0):
        """
        Return x, y grid-coordinates of trajectory based on starting point.

        Integrate both forward and backward in time from starting point in
        grid coordinates.

        Integration is terminated when a trajectory reaches a domain boundary
        or when it crosses into an already occupied cell in the StreamMask. The
        resulting trajectory is None if it is shorter than `minlength`.
        """

        stotal, x_traj, y_traj = 0., [], []

        try:
            dmap.start_trajectory(x0, y0)
        except InvalidIndexError:
            return None
        if integration_direction in ['both', 'backward']:
            s, xt, yt = _integrate_rk12(x0, y0, dmap, backward_time, maxlength)
            stotal += s
            x_traj += xt[::-1]
            y_traj += yt[::-1]

        if integration_direction in ['both', 'forward']:
            dmap.reset_start_point(x0, y0)
            s, xt, yt = _integrate_rk12(x0, y0, dmap, forward_time, maxlength)
            if len(x_traj) > 0:
                xt = xt[1:]
                yt = yt[1:]
            stotal += s
            x_traj += xt
            y_traj += yt

        if stotal > minlength:
            return x_traj, y_traj
        else:  # reject short trajectories
            dmap.undo_trajectory()
            return None

    return integrate
