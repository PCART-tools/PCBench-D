def stop():
    check_error(cudart().cudaProfilerStop())
