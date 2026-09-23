def run_subprocess(args):
    seed, env, sub_label, extra_env_vars = args
    core_str = None
    try:
        core_str, result_file, num_threads = _WORKER_POOL.get()
        with open(result_file, "wb"):
            pass

        env_vars: Dict[str, str] = {
            "PATH": os.getenv("PATH") or "",
            "PYTHONPATH": os.getenv("PYTHONPATH") or "",

            # NumPy
            "OMP_NUM_THREADS": str(num_threads),
            "MKL_NUM_THREADS": str(num_threads),
            "NUMEXPR_NUM_THREADS": str(num_threads),
        }
        env_vars.update(extra_env_vars or {})

        subprocess.run(
            f"source activate {env} && "
            f"taskset --cpu-list {core_str} "
            f"python {os.path.abspath(__file__)} "
            "--DETAIL_in_subprocess "
            f"--DETAIL_seed {seed} "
            f"--DETAIL_num_threads {num_threads} "
            f"--DETAIL_sub_label '{sub_label}' "
            f"--DETAIL_result_file {result_file} "
            f"--DETAIL_env {env}",
            env=env_vars,
            stdout=subprocess.PIPE,
            shell=True
        )

        with open(result_file, "rb") as f:
            result_bytes = f.read()

        with _RESULT_FILE_LOCK, \
             open(RESULT_FILE, "ab") as f:
            f.write(result_bytes)

    except KeyboardInterrupt:
        pass  # Handle ctrl-c gracefully.

    finally:
        if core_str is not None:
            _WORKER_POOL.put((core_str, result_file, num_threads))
