def read_graph(name):
    dirname = os.path.dirname(__file__)
    fname = os.path.join(dirname, name + ".gpickle.bz2")
    with bz2.BZ2File(fname, "rb") as f:
        G = pickle.load(f)
    return G
