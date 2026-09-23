@image_comparison(['rgba_alpha.png'], remove_text=True,
                  tol=0 if platform.machine() == 'x86_64' else 0.01)
def test_alpha_rgba():
    fig, ax = plt.subplots()
    ax.plot(range(10), lw=5)
    leg = plt.legend(['Longlabel that will go away'], loc='center')
    leg.legendPatch.set_facecolor([1, 0, 0, 0.5])
