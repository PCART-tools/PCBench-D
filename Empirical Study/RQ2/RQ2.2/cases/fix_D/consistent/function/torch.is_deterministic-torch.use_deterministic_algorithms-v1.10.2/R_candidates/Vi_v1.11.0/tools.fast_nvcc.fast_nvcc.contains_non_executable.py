def contains_non_executable(commands: List[str]) -> bool:
    for command in commands:
        # This is to deal with special command dry-run result from NVCC such as:
        # ```
        # #$ "/lib64/ccache"/c++ -std=c++11 -E -x c++ -D__CUDACC__ -D__NVCC__  -fPIC -fvisibility=hidden -O3 \
        #   -I ... -m64 "reduce_scatter.cu" > "/tmp/tmpxft_0037fae3_00000000-5_reduce_scatter.cpp4.ii
        # #$ -- Filter Dependencies -- > ... pytorch/build/nccl/obj/collectives/device/reduce_scatter.dep.tmp
        # ```
        if command.startswith("--"):
            return True
    return False
