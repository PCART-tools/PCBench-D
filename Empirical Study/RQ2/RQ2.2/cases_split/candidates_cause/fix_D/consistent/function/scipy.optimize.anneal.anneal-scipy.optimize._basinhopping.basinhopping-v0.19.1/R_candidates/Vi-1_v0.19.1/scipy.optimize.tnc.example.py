    def example():
        print("Example")

        # A function to minimize
        def function(x):
            f = pow(x[0],2.0)+pow(abs(x[1]),3.0)
            g = [0,0]
            g[0] = 2.0*x[0]
            g[1] = 3.0*pow(abs(x[1]),2.0)
            if x[1] < 0:
                g[1] = -g[1]
            return f, g

        # Optimizer call
        x, nf, rc = fmin_tnc(function, [-7, 3], bounds=([-10, 1], [10, 10]))

        print("After", nf, "function evaluations, TNC returned:", RCSTRINGS[rc])
        print("x =", x)
        print("exact value = [0, 1]")
        print()
