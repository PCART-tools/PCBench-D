def requires_mpi():
    return sandcastle_skip_if(
        not c10d.is_mpi_available(),
        "c10d was not compiled with the MPI backend",
    )
