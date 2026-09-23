@image_comparison(['logscale_mask.png'], remove_text=True)
def test_logscale_mask():
    # Check that zero values are masked correctly on log scales.
    # See github issue 8045
    xs = np.linspace(0, 50, 1001)

    fig, ax = plt.subplots()
    ax.plot(np.exp(-xs**2))
    fig.canvas.draw()
    ax.set(yscale="log")
