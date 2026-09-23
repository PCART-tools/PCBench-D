def test_extend_colorbar_customnorm():
    # This was a funny error with TwoSlopeNorm, maybe with other norms,
    # when extend='both'
    fig, (ax0, ax1) = plt.subplots(2, 1)
    pcm = ax0.pcolormesh([[0]], norm=TwoSlopeNorm(vcenter=0., vmin=-2, vmax=1))
    cb = fig.colorbar(pcm, ax=ax0, extend='both')
    np.testing.assert_allclose(cb.ax.get_position().extents,
                               [0.78375, 0.536364, 0.796147, 0.9], rtol=1e-3)
