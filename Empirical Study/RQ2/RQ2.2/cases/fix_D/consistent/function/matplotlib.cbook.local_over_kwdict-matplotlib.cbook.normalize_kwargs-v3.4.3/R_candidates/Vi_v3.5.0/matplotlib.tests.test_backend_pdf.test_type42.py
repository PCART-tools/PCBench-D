def test_type42():
    rcParams['pdf.fonttype'] = 42

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3])
    fig.savefig(io.BytesIO())
