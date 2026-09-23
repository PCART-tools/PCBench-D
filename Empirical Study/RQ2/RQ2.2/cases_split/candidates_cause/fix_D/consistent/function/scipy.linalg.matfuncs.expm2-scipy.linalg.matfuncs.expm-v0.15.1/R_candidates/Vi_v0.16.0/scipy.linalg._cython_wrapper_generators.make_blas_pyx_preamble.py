def make_blas_pyx_preamble(all_sigs):
    names = [sig[0] for sig in all_sigs]
    return blas_pyx_preamble.format("\n- ".join(names))
