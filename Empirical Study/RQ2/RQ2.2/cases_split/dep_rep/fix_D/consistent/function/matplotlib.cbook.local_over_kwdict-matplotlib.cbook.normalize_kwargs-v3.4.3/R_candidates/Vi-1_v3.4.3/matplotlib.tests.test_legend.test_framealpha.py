@image_comparison(['framealpha'], remove_text=True,
                  tol=0 if platform.machine() == 'x86_64' else 0.02)
def test_framealpha():
    x = np.linspace(1, 100, 100)
    y = x
    plt.plot(x, y, label='mylabel', lw=10)
    plt.legend(framealpha=0.5)
