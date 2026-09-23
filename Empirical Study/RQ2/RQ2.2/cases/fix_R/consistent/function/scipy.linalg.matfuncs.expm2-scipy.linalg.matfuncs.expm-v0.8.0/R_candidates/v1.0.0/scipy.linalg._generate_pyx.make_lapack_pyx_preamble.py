def make_lapack_pyx_preamble(all_sigs):
    names = [sig[0] for sig in all_sigs]
    return lapack_pyx_preamble.format("\n- ".join(names))
