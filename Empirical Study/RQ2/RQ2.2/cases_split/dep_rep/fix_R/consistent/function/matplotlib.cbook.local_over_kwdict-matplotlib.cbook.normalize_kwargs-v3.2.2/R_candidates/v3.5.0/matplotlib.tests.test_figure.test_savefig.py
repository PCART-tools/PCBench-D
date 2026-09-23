def test_savefig():
    fig = plt.figure()
    msg = r"savefig\(\) takes 2 positional arguments but 3 were given"
    with pytest.raises(TypeError, match=msg):
        fig.savefig("fname1.png", "fname2.png")
