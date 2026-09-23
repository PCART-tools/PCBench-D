def post_pytorch_comment(pr_number: int, merger: str) -> Any:
    message = {'body' : f"Hey {merger}." + """
You've committed this PR, but it does not have both a 'release notes: ...' and 'topics: ...' label. \
Please add one of each to the PR. The 'release notes: ...' label should represent the part of \
PyTorch that this PR changes (fx, autograd, distributed, etc) and the 'topics: ...' label should \
represent the kind of PR it is (not user facing, new feature, bug fix, perf improvement, etc). \
The list of valid labels can be found [here](https://github.com/pytorch/pytorch/labels?q=release+notes) \
for the 'release notes: ...' and [here](https://github.com/pytorch/pytorch/labels?q=topic) for the \
'topics: ...'.
For changes that are 'topic: not user facing' there is no need for a release notes label."""}

    response = requests.post(
        f"{PYTORCH_REPO}/issues/{pr_number}/comments",
        json.dumps(message),
        headers=REQUEST_HEADERS)
    return response.json()
