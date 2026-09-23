def test_textcomp_full():
    plt.rcParams["text.latex.preamble"] = r"\usepackage[full]{textcomp}"
    fig = plt.figure()
    fig.text(.5, .5, "hello, world", usetex=True)
    fig.canvas.draw()
