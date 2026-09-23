def generate_blas_pxd(all_sigs):
    body = '\n'.join(pxd_decl(*sig) for sig in all_sigs)
    return blas_pxd_preamble + body
