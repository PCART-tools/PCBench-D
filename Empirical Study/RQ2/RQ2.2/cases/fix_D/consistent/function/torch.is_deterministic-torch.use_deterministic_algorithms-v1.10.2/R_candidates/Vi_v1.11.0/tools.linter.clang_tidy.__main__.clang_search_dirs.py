def clang_search_dirs() -> List[str]:
    # Compilers are ordered based on fallback preference
    # We pick the first one that is available on the system
    compilers = ["clang", "gcc", "cpp", "cc"]
    compilers = [c for c in compilers if shutil.which(c) is not None]
    if len(compilers) == 0:
        raise RuntimeError(f"None of {compilers} were found")
    compiler = compilers[0]

    result = subprocess.run(
        [compiler, "-E", "-x", "c++", "-", "-v"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    stderr = result.stderr.decode().strip().split("\n")
    search_start = r"#include.*search starts here:"
    search_end = r"End of search list."

    append_path = False
    search_paths = []
    for line in stderr:
        if re.match(search_start, line):
            if append_path:
                continue
            else:
                append_path = True
        elif re.match(search_end, line):
            break
        elif append_path:
            search_paths.append(line.strip())

    # There are source files include <torch/cuda.h>, <torch/torch.h> etc.
    # under torch/csrc/api/include folder. Since torch/csrc/api/include is not
    # a search path for clang-tidy, there will be clang-disagnostic errors
    # complaing those header files not found. Change the source code to include
    # full path like torch/csrc/api/include/torch/torch.h does not work well
    # since torch/torch.h includes torch/all.h which inturn includes more.
    # We would need recursively change mutliple files.
    # Adding the include path to the lint script should be a better solution.
    search_paths.append(
        os.path.join(PYTORCH_ROOT, "torch/csrc/api/include"),
    )
    return search_paths
