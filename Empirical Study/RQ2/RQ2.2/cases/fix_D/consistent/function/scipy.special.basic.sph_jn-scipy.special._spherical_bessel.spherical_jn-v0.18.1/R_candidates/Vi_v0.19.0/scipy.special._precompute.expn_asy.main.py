def main():
    print(__doc__)
    fn = os.path.join('..', 'cephes', 'expn.h')

    K = 12
    A = generate_A(K)
    with open(fn + '.new', 'w') as f:
        f.write(WARNING)
        f.write("#define nA {}\n".format(len(A)))
        for k, Ak in enumerate(A):
            tmp = ', '.join([str(x.evalf(18)) for x in Ak.coeffs()])
            f.write("double A{}[] = {{{}}};\n".format(k, tmp))
        tmp = ", ".join(["A{}".format(k) for k in range(K + 1)])
        f.write("double *A[] = {{{}}};\n".format(tmp))
        tmp = ", ".join([str(Ak.degree()) for Ak in A])
        f.write("int Adegs[] = {{{}}};\n".format(tmp))
    os.rename(fn + '.new', fn)
