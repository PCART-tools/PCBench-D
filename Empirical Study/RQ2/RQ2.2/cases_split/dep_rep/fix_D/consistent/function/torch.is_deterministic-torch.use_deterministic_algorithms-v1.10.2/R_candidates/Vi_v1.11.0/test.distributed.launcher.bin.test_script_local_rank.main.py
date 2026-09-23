def main():
    print("Start execution")
    args = parse_args()
    expected_rank = int(os.environ["LOCAL_RANK"])
    actual_rank = args.local_rank
    if expected_rank != actual_rank:
        raise RuntimeError(
            "Parameters passed: --local_rank that has different value "
            f"from env var: expected: {expected_rank}, got: {actual_rank}"
        )
    print("End execution")
