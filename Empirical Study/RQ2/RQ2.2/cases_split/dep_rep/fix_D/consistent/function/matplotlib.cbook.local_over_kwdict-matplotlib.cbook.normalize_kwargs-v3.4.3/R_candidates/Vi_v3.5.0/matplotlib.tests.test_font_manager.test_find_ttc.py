def test_find_ttc():
    fp = FontProperties(family=["WenQuanYi Zen Hei"])
    if Path(findfont(fp)).name != "wqy-zenhei.ttc":
        pytest.skip("Font may be missing")

    fig, ax = plt.subplots()
    ax.text(.5, .5, "\N{KANGXI RADICAL DRAGON}", fontproperties=fp)
    for fmt in ["raw", "svg", "pdf", "ps"]:
        fig.savefig(BytesIO(), format=fmt)
