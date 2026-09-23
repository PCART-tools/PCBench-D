def generate_fortran(func_sigs):
    return "\n".join(fort_subroutine_wrapper(*sig) for sig in func_sigs)
