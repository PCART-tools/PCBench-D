def get_dep_modules(test: str) -> Set[str]:
    # Cache results in case of repetition
    if test in _DEP_MODULES_CACHE:
        return _DEP_MODULES_CACHE[test]

    test_location = REPO_ROOT / "test" / f"{test}.py"

    # HACK: some platforms default to ascii, so we can't just run_script :(
    finder = modulefinder.ModuleFinder(
        # Ideally exclude all third party modules, to speed up calculation.
        excludes=[
            "scipy",
            "numpy",
            "numba",
            "multiprocessing",
            "sklearn",
            "setuptools",
            "hypothesis",
            "llvmlite",
            "joblib",
            "email",
            "importlib",
            "unittest",
            "urllib",
            "json",
            "collections",
            # Modules below are excluded because they are hitting https://bugs.python.org/issue40350
            # Trigger AttributeError: 'NoneType' object has no attribute 'is_package'
            "mpl_toolkits",
            "google",
            "onnx",
            # Triggers RecursionError
            "mypy",
        ],
    )

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        finder.run_script(str(test_location))
    dep_modules = set(finder.modules.keys())
    _DEP_MODULES_CACHE[test] = dep_modules
    return dep_modules
