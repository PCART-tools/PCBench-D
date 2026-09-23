def set_mkl_threads(num_threads):
    existing_value = os.environ.get('MKL_NUM_THREADS', '')
    if existing_value != '':
        print("Overwriting existing MKL_NUM_THREADS value: {}; Setting it to {}.".format(
            existing_value, num_threads))
    os.environ["MKL_NUM_THREADS"] = str(num_threads)
