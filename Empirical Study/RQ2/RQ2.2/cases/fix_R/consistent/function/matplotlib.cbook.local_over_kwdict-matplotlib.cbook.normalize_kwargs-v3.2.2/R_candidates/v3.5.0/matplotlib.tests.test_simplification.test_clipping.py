@image_comparison(['clipping'], remove_text=True)
def test_clipping():
    t = np.arange(0.0, 2.0, 0.01)
    s = np.sin(2*np.pi*t)

    fig, ax = plt.subplots()
    ax.plot(t, s, linewidth=1.0)
    ax.set_ylim((-0.20, -0.28))
