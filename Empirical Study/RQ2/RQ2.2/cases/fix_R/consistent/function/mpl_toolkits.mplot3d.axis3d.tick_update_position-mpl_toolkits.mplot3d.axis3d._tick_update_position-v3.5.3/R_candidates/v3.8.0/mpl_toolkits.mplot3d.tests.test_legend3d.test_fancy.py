@image_comparison(['fancy.png'], remove_text=True, style=('mpl20'))
def test_fancy():
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    ax.plot(np.arange(10), np.full(10, 5), np.full(10, 5), 'o--', label='line')
    ax.scatter(np.arange(10), np.arange(10, 0, -1), label='scatter')
    ax.errorbar(np.full(10, 5), np.arange(10), np.full(10, 10),
                xerr=0.5, zerr=0.5, label='errorbar')
    ax.legend(loc='lower left', ncols=2, title='My legend', numpoints=1)
