def generate_lapack_pxd(all_sigs):
    return lapack_pxd_preamble + '\n'.join(pxd_decl(*sig) for sig in all_sigs)
