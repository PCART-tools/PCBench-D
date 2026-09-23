def get_disabled_tests(dirpath: str, filename: str = DISABLED_TESTS_FILE) -> Optional[Dict[str, Any]]:
    def process_disabled_test(the_response: Dict[str, Any]) -> Dict[str, Any]:
        disabled_test_from_issues = dict()
        for item in the_response['items']:
            title = item['title']
            key = 'DISABLED '
            issue_url = item['html_url']
            issue_number = issue_url.split('/')[-1]
            if title.startswith(key) and issue_number not in IGNORE_DISABLED_ISSUES:
                test_name = title[len(key):].strip()
                body = item['body']
                platforms_to_skip = []
                key = 'platforms:'
                for line in body.splitlines():
                    line = line.lower()
                    if line.startswith(key):
                        pattern = re.compile(r"^\s+|\s*,\s*|\s+$")
                        platforms_to_skip.extend([x for x in pattern.split(line[len(key):]) if x])
                disabled_test_from_issues[test_name] = (item['html_url'], platforms_to_skip)
        return disabled_test_from_issues
    try:
        url = 'https://raw.githubusercontent.com/pytorch/test-infra/main/stats/disabled-tests.json'
        return fetch_and_cache(dirpath, filename, url, process_disabled_test)
    except Exception:
        print("Couldn't download test skip set, leaving all tests enabled...")
        return {}
