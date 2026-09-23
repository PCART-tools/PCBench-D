def main():
    print(__doc__)
    K = 25
    N = 25
    with mp.workdps(50):
        d = compute_d(K, N)
    fn = os.path.join(os.path.dirname(__file__), '..', 'cephes', 'igam.h')
    with open(fn + '.new', 'w') as f:
        f.write(header.format(K, N))
        for k, row in enumerate(d):
            row = map(lambda x: mp.nstr(x, 17, min_fixed=0, max_fixed=0), row)
            f.write('{')
            f.write(", ".join(row))
            if k < K - 1:
                f.write('},\n')
            else:
                f.write('}};\n')
        f.write(footer)
    os.rename(fn + '.new', fn)
