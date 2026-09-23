    def test_apply_window_hanning_2D_stack_windows_axis1_unflatten(self):
        n = 32
        ydata = np.arange(n)
        ydata1 = ydata+5
        ydata2 = ydata+3.3
        ycontrol1 = _apply_window(ydata1, mlab.window_hanning)
        ycontrol2 = mlab.window_hanning(ydata2)
        ydata = np.vstack([ydata1, ydata2])
        ycontrol = np.vstack([ycontrol1, ycontrol2])
        ydata = np.tile(ydata, (20, 1))
        ycontrol = np.tile(ycontrol, (20, 1))
        ydata = ydata.flatten()
        ydata1 = mlab.stride_windows(ydata, 32, noverlap=0, axis=0)
        result = _apply_window(ydata1, mlab.window_hanning, axis=0,
                               return_window=False)
        assert_allclose(ycontrol.T, result, atol=1e-08)
