def get_test_infra_slow_tests() -> Dict[str, float]:
    url = "https://raw.githubusercontent.com/pytorch/test-infra/main/stats/slow-tests.json"
    contents = urlopen(url, timeout=1).read().decode('utf-8')
    return cast(Dict[str, float], json.loads(contents))
