@image_comparison(['antialiased.png'])
def test_antialiasing():
    mpl.rcParams['text.antialiased'] = True

    fig = plt.figure(figsize=(5.25, 0.75))
    fig.text(0.5, 0.75, "antialiased", horizontalalignment='center',
             verticalalignment='center')
    fig.text(0.5, 0.25, r"$\sqrt{x}$", horizontalalignment='center',
             verticalalignment='center')
