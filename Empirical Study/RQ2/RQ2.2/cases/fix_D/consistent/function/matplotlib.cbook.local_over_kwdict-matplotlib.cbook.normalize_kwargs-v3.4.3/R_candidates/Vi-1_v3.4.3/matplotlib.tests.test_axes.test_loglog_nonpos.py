@pytest.mark.parametrize("new_api", [False, True])
@image_comparison(["test_loglog_nonpos.png"], remove_text=True, style='mpl20')
def test_loglog_nonpos(new_api):
    fig, axs = plt.subplots(3, 3)
    x = np.arange(1, 11)
    y = x**3
    y[7] = -3.
    x[4] = -10
    for (i, j), ax in np.ndenumerate(axs):
        mcx = ['mask', 'clip', ''][j]
        mcy = ['mask', 'clip', ''][i]
        if new_api:
            if mcx == mcy:
                if mcx:
                    ax.loglog(x, y**3, lw=2, nonpositive=mcx)
                else:
                    ax.loglog(x, y**3, lw=2)
            else:
                ax.loglog(x, y**3, lw=2)
                if mcx:
                    ax.set_xscale("log", nonpositive=mcx)
                if mcy:
                    ax.set_yscale("log", nonpositive=mcy)
        else:
            kws = {}
            if mcx:
                kws['nonposx'] = mcx
            if mcy:
                kws['nonposy'] = mcy
            with (pytest.warns(MatplotlibDeprecationWarning) if kws
                  else nullcontext()):
                ax.loglog(x, y**3, lw=2, **kws)
