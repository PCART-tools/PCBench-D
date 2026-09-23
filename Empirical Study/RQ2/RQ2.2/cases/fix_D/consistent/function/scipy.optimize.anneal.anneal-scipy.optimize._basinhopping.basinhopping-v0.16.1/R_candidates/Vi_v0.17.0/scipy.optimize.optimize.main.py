def main():
    import time

    times = []
    algor = []
    x0 = [0.8, 1.2, 0.7]
    print("Nelder-Mead Simplex")
    print("===================")
    start = time.time()
    x = fmin(rosen, x0)
    print(x)
    times.append(time.time() - start)
    algor.append('Nelder-Mead Simplex\t')

    print()
    print("Powell Direction Set Method")
    print("===========================")
    start = time.time()
    x = fmin_powell(rosen, x0)
    print(x)
    times.append(time.time() - start)
    algor.append('Powell Direction Set Method.')

    print()
    print("Nonlinear CG")
    print("============")
    start = time.time()
    x = fmin_cg(rosen, x0, fprime=rosen_der, maxiter=200)
    print(x)
    times.append(time.time() - start)
    algor.append('Nonlinear CG     \t')

    print()
    print("BFGS Quasi-Newton")
    print("=================")
    start = time.time()
    x = fmin_bfgs(rosen, x0, fprime=rosen_der, maxiter=80)
    print(x)
    times.append(time.time() - start)
    algor.append('BFGS Quasi-Newton\t')

    print()
    print("BFGS approximate gradient")
    print("=========================")
    start = time.time()
    x = fmin_bfgs(rosen, x0, gtol=1e-4, maxiter=100)
    print(x)
    times.append(time.time() - start)
    algor.append('BFGS without gradient\t')

    print()
    print("Newton-CG with Hessian product")
    print("==============================")
    start = time.time()
    x = fmin_ncg(rosen, x0, rosen_der, fhess_p=rosen_hess_prod, maxiter=80)
    print(x)
    times.append(time.time() - start)
    algor.append('Newton-CG with hessian product')

    print()
    print("Newton-CG with full Hessian")
    print("===========================")
    start = time.time()
    x = fmin_ncg(rosen, x0, rosen_der, fhess=rosen_hess, maxiter=80)
    print(x)
    times.append(time.time() - start)
    algor.append('Newton-CG with full hessian')

    print()
    print("\nMinimizing the Rosenbrock function of order 3\n")
    print(" Algorithm \t\t\t       Seconds")
    print("===========\t\t\t      =========")
    for k in range(len(algor)):
        print(algor[k], "\t -- ", times[k])
