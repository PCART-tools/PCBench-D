@image_comparison(baseline_images=['panecolor_rcparams.png'],
                  remove_text=True,
                  style='mpl20')
def test_panecolor_rcparams():
    with plt.rc_context({'axes3d.xaxis.panecolor': 'r',
                         'axes3d.yaxis.panecolor': 'g',
                         'axes3d.zaxis.panecolor': 'b'}):
        fig = plt.figure(figsize=(1, 1))
        fig.add_subplot(projection='3d')
