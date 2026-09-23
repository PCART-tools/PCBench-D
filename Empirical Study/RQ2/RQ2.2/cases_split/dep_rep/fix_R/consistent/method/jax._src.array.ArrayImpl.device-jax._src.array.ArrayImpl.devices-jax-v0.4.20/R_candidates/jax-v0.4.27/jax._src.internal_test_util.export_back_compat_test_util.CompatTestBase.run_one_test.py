  def run_one_test(self, func: Callable[..., jax.Array],
                   data: CompatTestData,
                   polymorphic_shapes: Sequence[str] | None = None,
                   rtol: float | None = None,
                   atol: float | None = None,
                   allow_unstable_custom_call_targets: Sequence[str] = (),
                   check_results: Callable[..., None] | None = None,
                   expect_current_custom_calls: Sequence[str] | None = None):
    """Run one compatibility test.

    Args:
      func: the JAX function to serialize and run
      data: the test data
      polymorphic_shapes: when using shape polymorphism, the specification for
        each argument of `func`.
      rtol: relative tolerance for numerical comparisons
      atol: absolute tolerance for numerical comparisons
      check_results: invoked with the results obtained from running the
        serialized code, and those stored in the test data, and the kwargs rtol
        and atol.
      allow_unstable_custom_call_targets: additional custom call targets to allow.
      expect_current_custom_calls: if `None` checks that the current serialization
        has the same custom calls as the saved one. This is the default, and
        will fail when the serialization changes. Otherwise, when checking old
        serializations you can specify what custom calls are expected in the
        current serialization.
      nr_devices: the number of devices for which the data was serialized.
    """
    if not isinstance(data, CompatTestData):
      raise ValueError(f"Expecting data: CompatTestData but got {data}. "
                       "Did you forget to `self.load_testdata`?")

    if self.default_jax_backend() != data.platform:
      self.skipTest(f"Test enabled only for {data.platform}")

    logging.info("Lowering and running the function at the current version")
    res_run_current = self.run_current(func, data)
    if not isinstance(res_run_current, (list, tuple)):
      res_run_current = (res_run_current,)
    res_run_current = tuple(np.array(a) for a in res_run_current)
    logging.info("Result of current version run is %s", res_run_current)

    serialized, module_str, module_version, nr_devices = self.serialize(
      func, data,
      polymorphic_shapes=polymorphic_shapes,
      allow_unstable_custom_call_targets=allow_unstable_custom_call_targets)

    custom_call_re = r"stablehlo.custom_call\s*@([^\(]+)\("
    current_custom_call_targets = sorted(
        set(re.findall(custom_call_re, module_str)))

    np.set_printoptions(threshold=sys.maxsize, floatmode="unique")
    # Print the current test data to simplify updating the test.
    updated_testdata = f"""
# Pasted from the test output (see export_back_compat_test_util.py module docstring)
data_{datetime.date.today().strftime('%Y_%m_%d')} = dict(
    testdata_version={CURRENT_TESTDATA_VERSION},
    platform={self.default_jax_backend()!r},
    custom_call_targets={current_custom_call_targets!r},
    serialized_date={datetime.date.today()!r},
    inputs={data.inputs!r},
    expected_outputs={res_run_current!r},
    mlir_module_text=r\"\"\"\n{module_str}\"\"\",
    mlir_module_serialized={serialized!r},
    xla_call_module_version={module_version},
    nr_devices={nr_devices},
)  # End paste

"""
    # Replace the word that should not appear.
    updated_testdata = re.sub(r"google.", "googlex", updated_testdata)
    output_dir = os.getenv("TEST_UNDECLARED_OUTPUTS_DIR",
                           "/tmp/back_compat_testdata")
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    output_file = os.path.join(output_dir, f"{self._testMethodName}.py")
    logging.info("Writing the updated testdata at %s", output_file)
    with open(output_file, "w") as f:
      f.write(updated_testdata)

    if rtol is None:
      rtol = 1.e-7
    if check_results is not None:
      check_results(res_run_current, data.expected_outputs, rtol=rtol,
                    atol=atol)
    else:
      self.assertAllClose(res_run_current, data.expected_outputs, rtol=rtol,
                          atol=atol)

    logging.info("Running the serialized module")
    res_run_serialized = self.run_serialized(
        data,
        polymorphic_shapes=polymorphic_shapes)
    logging.info("Result of serialized run is %s", res_run_serialized)
    if check_results is not None:
      check_results(res_run_serialized, data.expected_outputs,
                    rtol=rtol, atol=atol)
    else:
      self.assertAllClose(res_run_serialized, data.expected_outputs,
                          rtol=rtol, atol=atol)
    if expect_current_custom_calls is None:
      expect_current_custom_calls = data.custom_call_targets
    self.assertItemsEqual(expect_current_custom_calls, current_custom_call_targets)
