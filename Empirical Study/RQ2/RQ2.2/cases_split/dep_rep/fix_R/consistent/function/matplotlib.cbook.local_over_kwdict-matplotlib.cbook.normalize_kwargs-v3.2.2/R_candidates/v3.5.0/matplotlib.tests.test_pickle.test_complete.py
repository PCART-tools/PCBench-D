@image_comparison(
    ['multi_pickle.png'], remove_text=True, style='mpl20', tol=0.082)
def test_complete():
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    fig = plt.figure('Figure with a label?', figsize=(10, 6))

    plt.suptitle('Can you fit any more in a figure?')

    # make some arbitrary data
    x, y = np.arange(8), np.arange(10)
    data = u = v = np.linspace(0, 10, 80).reshape(10, 8)
    v = np.sin(v * -0.6)

    # Ensure lists also pickle correctly.
    plt.subplot(3, 3, 1)
    plt.plot(list(range(10)))

    plt.subplot(3, 3, 2)
    plt.contourf(data, hatches=['//', 'ooo'])
    plt.colorbar()

    plt.subplot(3, 3, 3)
    plt.pcolormesh(data)

    plt.subplot(3, 3, 4)
    plt.imshow(data)

    plt.subplot(3, 3, 5)
    plt.pcolor(data)

    ax = plt.subplot(3, 3, 6)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 9)
    plt.streamplot(x, y, u, v)

    ax = plt.subplot(3, 3, 7)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 9)
    plt.quiver(x, y, u, v)

    plt.subplot(3, 3, 8)
    plt.scatter(x, x**2, label='$x^2$')
    plt.legend(loc='upper left')

    plt.subplot(3, 3, 9)
    plt.errorbar(x, x * -0.5, xerr=0.2, yerr=0.4)

    #
    # plotting is done, now test its pickle-ability
    #
    result_fh = BytesIO()
    pickle.dump(fig, result_fh, pickle.HIGHEST_PROTOCOL)

    plt.close('all')

    # make doubly sure that there are no figures left
    assert plt._pylab_helpers.Gcf.figs == {}

    # wind back the fh and load in the figure
    result_fh.seek(0)
    fig = pickle.load(result_fh)

    # make sure there is now a figure manager
    assert plt._pylab_helpers.Gcf.figs != {}

    assert fig.get_label() == 'Figure with a label?'
