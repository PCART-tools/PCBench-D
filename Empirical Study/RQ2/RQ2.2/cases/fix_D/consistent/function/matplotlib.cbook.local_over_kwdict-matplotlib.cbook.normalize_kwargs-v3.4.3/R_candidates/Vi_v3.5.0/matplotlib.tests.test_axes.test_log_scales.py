@image_comparison(['log_scales'])
def test_log_scales():
    fig, ax = plt.subplots()
    ax.plot(np.log(np.linspace(0.1, 100)))
    ax.set_yscale('log', base=5.5)
    ax.invert_yaxis()
    ax.set_xscale('log', base=9.0)
