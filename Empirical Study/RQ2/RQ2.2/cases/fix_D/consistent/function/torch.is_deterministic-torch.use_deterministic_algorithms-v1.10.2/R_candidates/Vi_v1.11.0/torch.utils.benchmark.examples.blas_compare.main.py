def main():
    with open(RESULT_FILE, "wb"):
        pass

    for num_threads in NUM_THREAD_SETTINGS:
        fill_core_pool(num_threads)
        workers = _WORKER_POOL.qsize()

        trials = []
        for seed in range(NUM_REPLICATES):
            for sub_label, env, extra_env_vars in BLAS_CONFIGS:
                env_path = os.path.join(blas_compare_setup.WORKING_ROOT, env)
                trials.append((seed, env_path, sub_label, extra_env_vars))

        n = len(trials)
        with multiprocessing.dummy.Pool(workers) as pool:
            start_time = time.time()
            for i, r in enumerate(pool.imap(run_subprocess, trials)):
                n_trials_done = i + 1
                time_per_result = (time.time() - start_time) / n_trials_done
                eta = int((n - n_trials_done) * time_per_result)
                print(f"\r{i + 1} / {n}    ETA:{datetime.timedelta(seconds=eta)}".ljust(80), end="")
                sys.stdout.flush()
        print(f"\r{n} / {n}  Total time: {datetime.timedelta(seconds=int(time.time() - start_time))}")
    print()

    # Any env will do, it just needs to have torch for benchmark utils.
    env_path = os.path.join(blas_compare_setup.WORKING_ROOT, BLAS_CONFIGS[0][1])
    subprocess.run(
        f"source activate {env_path} && "
        f"python {os.path.abspath(__file__)} "
        "--DETAIL_in_compare",
        shell=True
    )
