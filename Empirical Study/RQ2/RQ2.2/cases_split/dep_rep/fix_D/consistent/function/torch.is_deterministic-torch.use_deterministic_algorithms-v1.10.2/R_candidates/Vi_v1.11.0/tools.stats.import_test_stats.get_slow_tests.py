def get_slow_tests(dirpath: str, filename: str = SLOW_TESTS_FILE) -> Optional[Dict[str, float]]:
    url = "https://raw.githubusercontent.com/pytorch/test-infra/main/stats/slow-tests.json"
    try:
        return fetch_and_cache(dirpath, filename, url, lambda x: x)
    except Exception:
        print("Couldn't download slow test set, leaving all tests enabled...")
        return {}
