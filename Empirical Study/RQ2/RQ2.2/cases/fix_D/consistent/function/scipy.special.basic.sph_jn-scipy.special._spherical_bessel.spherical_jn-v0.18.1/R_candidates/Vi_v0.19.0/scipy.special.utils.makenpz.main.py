def main():
    p = OptionParser()
    options, args = p.parse_args()

    if len(args) != 1:
        p.error("no valid directory given")

    inp = args[0]
    outp = inp + ".npz"

    files = []
    for dirpath, dirnames, filenames in os.walk(inp):
        for fn in filenames:
            if fn.endswith('.txt'):
                files.append(
                    (dirpath[len(inp)+1:] + '/' + fn[:-4],
                     os.path.join(dirpath, fn)))

    data = {}
    for key, fn in files:
        key = key.replace('/', '-').strip('-')
        try:
            data[key] = np.loadtxt(fn)
        except ValueError:
            print("Failed to load", fn)

    savez_compress(outp, **data)
