def build_deps():
    report('-- Building version ' + version)

    check_submodules()
    check_pydep('yaml', 'pyyaml')

    build_caffe2(version=version,
                 cmake_python_library=cmake_python_library,
                 build_python=True,
                 rerun_cmake=RERUN_CMAKE,
                 cmake_only=CMAKE_ONLY,
                 cmake=cmake)

    if CMAKE_ONLY:
        report('Finished running cmake. Run "ccmake build" or '
               '"cmake-gui build" to adjust build options and '
               '"python setup.py install" to build.')
        sys.exit()

    # Use copies instead of symbolic files.
    # Windows has very poor support for them.
    sym_files = [
        'tools/shared/_utils_internal.py',
        'torch/utils/benchmark/utils/valgrind_wrapper/callgrind.h',
        'torch/utils/benchmark/utils/valgrind_wrapper/valgrind.h',
    ]
    orig_files = [
        'torch/_utils_internal.py',
        'third_party/valgrind-headers/callgrind.h',
        'third_party/valgrind-headers/valgrind.h',
    ]
    for sym_file, orig_file in zip(sym_files, orig_files):
        same = False
        if os.path.exists(sym_file):
            if filecmp.cmp(sym_file, orig_file):
                same = True
            else:
                os.remove(sym_file)
        if not same:
            shutil.copyfile(orig_file, sym_file)
