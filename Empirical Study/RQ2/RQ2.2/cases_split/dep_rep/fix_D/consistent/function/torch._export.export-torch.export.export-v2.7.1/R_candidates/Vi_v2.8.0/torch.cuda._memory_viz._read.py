    def _read(name):
        if name == "-":
            f = sys.stdin.buffer
        else:
            f = open(name, "rb")
        data = pickle.load(f)
        if isinstance(data, list):  # segments only...
            data = {"segments": data, "traces": []}
        return data
