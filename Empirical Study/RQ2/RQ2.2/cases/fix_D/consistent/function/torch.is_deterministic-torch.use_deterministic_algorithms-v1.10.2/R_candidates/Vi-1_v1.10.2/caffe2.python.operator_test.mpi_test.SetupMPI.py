def SetupMPI():
    try:
        # pyre-fixme[21]: undefined import
        from mpi4py import MPI
        global _has_mpi, COMM, RANK, SIZE
        _has_mpi = core.IsOperatorWithEngine("CreateCommonWorld", "MPI")
        COMM = MPI.COMM_WORLD
        RANK = COMM.Get_rank()
        SIZE = COMM.Get_size()
    except ImportError:
        _has_mpi = False
