def set_profile(profile: ParametricProfileNames | int) -> None:
    """
    Set the env var ``POLARS_HYPOTHESIS_PROFILE`` to the given profile name/value.

    Parameters
    ----------
    profile : {str, int}, optional
        Name of the profile to load; one of "fast", "balanced", "expensive", or
        the integer number of iterations to run (which will create and register
        a custom profile with that value).

    Examples
    --------
    >>> # prefer the 'balanced' profile for running parametric tests
    >>> from polars.testing.parametric.profiles import set_profile
    >>> set_profile("balanced")

    """
    profile_name = str(profile).split(".")[-1]
    if profile_name.replace("_", "").isdigit():
        profile_name = str(int(profile_name))

    else:
        from typing import get_args

        valid_profile_names = get_args(ParametricProfileNames)
        if profile_name not in valid_profile_names:
            raise ValueError(
                f"invalid profile name {profile_name!r}; expected one of {valid_profile_names!r}"
            )

    os.environ["POLARS_HYPOTHESIS_PROFILE"] = profile_name
