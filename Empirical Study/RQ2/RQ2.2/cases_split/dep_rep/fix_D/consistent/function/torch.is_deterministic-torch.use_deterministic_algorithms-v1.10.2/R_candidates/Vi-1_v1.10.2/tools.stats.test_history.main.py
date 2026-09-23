def main() -> None:
    for line in run(sys.argv[1:]):
        print(line, flush=True)
