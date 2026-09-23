def set_omp_threads(num_threads):
    existing_value = os.environ.get('OMP_NUM_THREADS', '')
    if existing_value != '':
        print("Overwriting existing OMP_NUM_THREADS value: {}; Setting it to {}.".format(
            existing_value, num_threads))
    os.environ["OMP_NUM_THREADS"] = str(num_threads)
