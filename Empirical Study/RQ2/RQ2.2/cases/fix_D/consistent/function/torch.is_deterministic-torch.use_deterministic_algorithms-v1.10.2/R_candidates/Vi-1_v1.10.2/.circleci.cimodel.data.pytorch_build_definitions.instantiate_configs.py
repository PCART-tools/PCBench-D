def instantiate_configs(only_slow_gradcheck):

    config_list = []

    root = get_root()
    found_configs = conf_tree.dfs(root)
    for fc in found_configs:

        restrict_phases = None
        distro_name = fc.find_prop("distro_name")
        compiler_name = fc.find_prop("compiler_name")
        compiler_version = fc.find_prop("compiler_version")
        is_xla = fc.find_prop("is_xla") or False
        is_asan = fc.find_prop("is_asan") or False
        is_coverage = fc.find_prop("is_coverage") or False
        is_noarch = fc.find_prop("is_noarch") or False
        is_onnx = fc.find_prop("is_onnx") or False
        is_pure_torch = fc.find_prop("is_pure_torch") or False
        is_vulkan = fc.find_prop("is_vulkan") or False
        is_slow_gradcheck = fc.find_prop("is_slow_gradcheck") or False
        parms_list_ignored_for_docker_image = []

        if only_slow_gradcheck ^ is_slow_gradcheck:
            continue

        python_version = None
        if compiler_name == "cuda" or compiler_name == "android":
            python_version = fc.find_prop("pyver")
            parms_list = [fc.find_prop("abbreviated_pyver")]
        else:
            parms_list = ["py" + fc.find_prop("pyver")]

        cuda_version = None
        rocm_version = None
        if compiler_name == "cuda":
            cuda_version = fc.find_prop("compiler_version")

        elif compiler_name == "rocm":
            rocm_version = fc.find_prop("compiler_version")
            restrict_phases = ["build", "test1", "test2", "caffe2_test"]

        elif compiler_name == "android":
            android_ndk_version = fc.find_prop("compiler_version")
            # TODO: do we need clang to compile host binaries like protoc?
            parms_list.append("clang5")
            parms_list.append("android-ndk-" + android_ndk_version)
            android_abi = fc.find_prop("android_abi")
            parms_list_ignored_for_docker_image.append(android_abi)
            restrict_phases = ["build"]

        elif compiler_name:
            gcc_version = compiler_name + (fc.find_prop("compiler_version") or "")
            parms_list.append(gcc_version)

        if is_asan:
            parms_list.append("asan")
            python_version = fc.find_prop("pyver")
            parms_list[0] = fc.find_prop("abbreviated_pyver")

        if is_coverage:
            parms_list_ignored_for_docker_image.append("coverage")
            python_version = fc.find_prop("pyver")

        if is_noarch:
            parms_list_ignored_for_docker_image.append("noarch")

        if is_onnx:
            parms_list.append("onnx")
            python_version = fc.find_prop("pyver")
            parms_list[0] = fc.find_prop("abbreviated_pyver")
            restrict_phases = ["build", "ort_test1", "ort_test2"]

        if cuda_version:
            cuda_gcc_version = fc.find_prop("cuda_gcc_override") or "gcc7"
            parms_list.append(cuda_gcc_version)

        is_libtorch = fc.find_prop("is_libtorch") or False
        is_important = fc.find_prop("is_important") or False
        parallel_backend = fc.find_prop("parallel_backend") or None
        build_only = fc.find_prop("build_only") or False
        shard_test = fc.find_prop("shard_test") or False
        # TODO: fix pure_torch python test packaging issue.
        if shard_test:
            restrict_phases = ["build"] if restrict_phases is None else restrict_phases
            restrict_phases.extend(["test1", "test2"])
        if build_only or is_pure_torch:
            restrict_phases = ["build"]

        if is_slow_gradcheck:
            parms_list_ignored_for_docker_image.append("old")
            parms_list_ignored_for_docker_image.append("gradcheck")

        gpu_resource = None
        if cuda_version and cuda_version != "10":
            gpu_resource = "medium"

        c = Conf(
            distro_name,
            parms_list,
            parms_list_ignored_for_docker_image,
            python_version,
            cuda_version,
            rocm_version,
            is_xla,
            is_vulkan,
            is_pure_torch,
            restrict_phases,
            gpu_resource,
            is_libtorch=is_libtorch,
            is_important=is_important,
            parallel_backend=parallel_backend,
            build_only=build_only,
        )

        # run docs builds on "pytorch-linux-xenial-py3.6-gcc5.4". Docs builds
        # should run on a CPU-only build that runs on all PRs.
        # XXX should this be updated to a more modern build? Projects are
        #     beginning to drop python3.6
        if (
            distro_name == "xenial"
            and fc.find_prop("pyver") == "3.6"
            and cuda_version is None
            and parallel_backend is None
            and not is_vulkan
            and not is_pure_torch
            and compiler_name == "gcc"
            and fc.find_prop("compiler_version") == "5.4"
        ):
            c.filters = gen_filter_dict(branches_list=r"/.*/",
                                        tags_list=RC_PATTERN)
            c.dependent_tests = gen_docs_configs(c)

        if (
            compiler_name != "clang"
            and not rocm_version
            and not is_libtorch
            and not is_vulkan
            and not is_pure_torch
            and not is_noarch
            and not is_slow_gradcheck
            and not only_slow_gradcheck
            and not build_only
        ):
            distributed_test = Conf(
                c.gen_build_name("") + "distributed",
                [],
                is_xla=False,
                restrict_phases=["test"],
                is_libtorch=False,
                is_important=True,
                parent_build=c,
            )
            c.dependent_tests.append(distributed_test)

        config_list.append(c)

    return config_list
