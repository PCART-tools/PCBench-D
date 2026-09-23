def check_test_type(test_type: str, target: str) -> None:
    if test_type in [TestType.CPP.value, TestType.PY.value]:
        return
    raise Exception(
        f"Can't parse test type: {test_type}.",
        f" Please check the type of buck target: {target}",
    )
