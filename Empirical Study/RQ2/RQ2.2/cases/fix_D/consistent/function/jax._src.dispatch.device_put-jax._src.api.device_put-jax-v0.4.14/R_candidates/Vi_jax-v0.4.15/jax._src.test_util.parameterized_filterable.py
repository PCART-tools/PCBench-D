def parameterized_filterable(*,
    kwargs: Sequence[dict[str, Any]],
    testcase_name: Optional[Callable[[dict[str, Any]], str]] = None,
    one_containing: Optional[str] = None,
):
  """
  Decorator for named parameterized tests, with filtering.

  Works like parameterized.named_parameters, except that it supports the
  `one_containing` option. This is useful to select only one of the tests,
  and to leave the test name unchanged (helps with specifying the desired test
  when debugging).

  Args:
    kwargs: Each entry is a set of kwargs to be passed to the test function.
    testcase_name: Optionally, a function to construct the testcase_name from
      one kwargs dict. If not given then kwarg may contain `testcase_name` and
      if not, the test case name is constructed as `str(kwarg)`.
      We sanitize the test names to work with -k test filters. See
      `sanitize_test_name`.
    one_containing: If given, then leave the test name unchanged, and use
      only one `kwargs` whose `testcase_name` includes `one_containing`.
  """
  # Ensure that all kwargs contain a testcase_name
  kwargs_with_testcase_name: Sequence[dict[str, Any]]
  if testcase_name is not None:
    kwargs_with_testcase_name = [
      dict(testcase_name=sanitize_test_name(str(testcase_name(kw))), **kw)
      for kw in kwargs]
  else:
    for kw in kwargs:
      testcase_name = kw.get("testcase_name")
      if testcase_name is None:
        testcase_name = "_".join(f"{k}={str(kw[k])}"  # type: ignore
                                 for k in sorted(kw.keys()))
      kw["testcase_name"] = sanitize_test_name(testcase_name)  # type: ignore

    kwargs_with_testcase_name = kwargs
  if one_containing is not None:
    filtered = tuple(kw for kw in kwargs_with_testcase_name
                     if one_containing in kw["testcase_name"])
    assert filtered, f"No testcase_name contains '{one_containing}'"
    kw = filtered[0]
    kw["testcase_name"] = ""
    return parameterized.named_parameters([kw])
  else:
    return parameterized.named_parameters(*kwargs_with_testcase_name)
