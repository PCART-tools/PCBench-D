def write(max: int, sleep: float, file: str):
    with open(file, "w") as fp:
        for i in range(max):
            print(i, file=fp, flush=True)
            time.sleep(sleep)
