@image_comparison(['streamplot_direction.png'],
                  remove_text=True, style='mpl20', tol=0.056)
def test_direction():
    x, y, U, V = swirl_velocity_field()
    plt.streamplot(x, y, U, V, integration_direction='backward',
                   maxlength=1.5, start_points=[[1.5, 0.]],
                   linewidth=2, density=2)
