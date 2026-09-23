@image_comparison(['polar_rlabel_position'], style='default')
def test_polar_rlabel_position():
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    ax.set_rlabel_position(315)
    ax.tick_params(rotation='auto')
