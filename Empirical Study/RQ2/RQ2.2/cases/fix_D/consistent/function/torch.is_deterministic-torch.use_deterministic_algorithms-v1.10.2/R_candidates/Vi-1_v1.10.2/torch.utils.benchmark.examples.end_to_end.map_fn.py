def map_fn(args):
    seed, envs, pr, use_gpu, finished_counts, test_variance = args
    gpu = _AVAILABLE_GPUS.get() if use_gpu else None
    try:
        _, result_file = tempfile.mkstemp(suffix=".pkl")
        for env in envs:
            cmd = _SUBPROCESS_CMD_TEMPLATE.format(
                source_env=envs[0] if test_variance else env,
                env=env, pr=pr, device=_GPU if use_gpu else _CPU,
                result_file=result_file, seed=seed,
            )
            run(cmd=cmd, cuda_visible_devices=gpu if use_gpu else "")
        finished_counts[_GPU if use_gpu else _CPU] += 1
        return (seed, use_gpu), read_results(result_file)
    except KeyboardInterrupt:
        pass  # Handle ctrl-c gracefully.
    finally:
        if gpu is not None:
            _AVAILABLE_GPUS.put(gpu)
        if os.path.exists(result_file):
            os.remove(result_file)
