def get_test_cases(directory):
    for root, _, files in os.walk(directory):
        for fname in files:
            if os.path.splitext(fname)[-1] == ".py":
                fullpath = os.path.join(root, fname)
                # Use relative path for nice py.test name
                relpath = os.path.relpath(fullpath, start=directory)

                yield pytest.param(
                    fullpath,
                    # Manually specify a name for the test
                    id=relpath,
                )
