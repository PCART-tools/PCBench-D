def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['conda', 'libtorch', 'wheels'])
    args = parser.parse_args()

    is_pr = is_pull_request()
    print(from_includes({
        'conda': generate_conda_matrix,
        'libtorch': generate_libtorch_matrix,
        'wheels': generate_wheels_matrix,
    }[args.mode](is_pr)))
