def _assert_z3_installed_if_tv_set():
    assert _HAS_Z3 or not config.translation_validation, (
        "translation validation requires Z3 package. Please, either install "
        "z3-solver or disable translation validation."
    )
