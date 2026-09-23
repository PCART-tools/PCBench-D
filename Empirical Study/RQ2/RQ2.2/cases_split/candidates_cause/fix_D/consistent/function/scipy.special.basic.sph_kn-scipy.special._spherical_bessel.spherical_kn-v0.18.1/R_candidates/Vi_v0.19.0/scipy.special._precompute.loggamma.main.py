def main():
    print(__doc__)
    print()
    stirling_coeffs = [mpmath.nstr(x, 20, min_fixed=0, max_fixed=0)
                       for x in stirling_series(8)[::-1]]
    taylor_coeffs = [mpmath.nstr(x, 20, min_fixed=0, max_fixed=0)
                     for x in taylor_series_at_1(23)[::-1]]
    print("Stirling series coefficients")
    print("----------------------------")
    print("\n".join(stirling_coeffs))
    print()
    print("Taylor series coefficients")
    print("--------------------------")
    print("\n".join(taylor_coeffs))
    print()
