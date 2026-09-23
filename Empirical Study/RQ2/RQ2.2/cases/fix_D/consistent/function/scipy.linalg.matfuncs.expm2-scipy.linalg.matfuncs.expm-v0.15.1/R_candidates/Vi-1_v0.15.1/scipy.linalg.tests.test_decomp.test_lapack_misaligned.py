@dec.knownfailureif(True, "Ticket #1152, triggers a segfault in rare cases.")
def test_lapack_misaligned():
    M = np.eye(10,dtype=float)
    R = np.arange(100)
    R.shape = 10,10
    S = np.arange(20000,dtype=np.uint8)
    S = np.frombuffer(S.data, offset=4, count=100, dtype=np.float)
    S.shape = 10, 10
    b = np.ones(10)
    v = np.ones(3,dtype=float)
    LU, piv = lu_factor(S)
    for (func, args, kwargs) in [
            (eig,(S,),dict(overwrite_a=True)),  # crash
            (eigvals,(S,),dict(overwrite_a=True)),  # no crash
            (lu,(S,),dict(overwrite_a=True)),  # no crash
            (lu_factor,(S,),dict(overwrite_a=True)),  # no crash
            (lu_solve,((LU,piv),b),dict(overwrite_b=True)),
            (solve,(S,b),dict(overwrite_a=True,overwrite_b=True)),
            (svd,(M,),dict(overwrite_a=True)),  # no crash
            (svd,(R,),dict(overwrite_a=True)),  # no crash
            (svd,(S,),dict(overwrite_a=True)),  # crash
            (svdvals,(S,),dict()),  # no crash
            (svdvals,(S,),dict(overwrite_a=True)),  # crash
            (cholesky,(M,),dict(overwrite_a=True)),  # no crash
            (qr,(S,),dict(overwrite_a=True)),  # crash
            (rq,(S,),dict(overwrite_a=True)),  # crash
            (hessenberg,(S,),dict(overwrite_a=True)),  # crash
            (schur,(S,),dict(overwrite_a=True)),  # crash
            ]:
        yield check_lapack_misaligned, func, args, kwargs
