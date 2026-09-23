class CompatTestBase(jtu.JaxTestCase):
  """Base class with helper functions for backward compatibility tests."""
  def default_jax_backend(self) -> str:
    # Canonicalize to turn into "cuda" or "rocm"
    return xb.canonicalize_platform(jax.default_backend())

  def starter_data(self, inputs: Sequence[np.ndarray]) -> CompatTestData:
    # Helper for starting a test, see module docstring.
    assert isinstance(inputs, Sequence), f"{inputs}"
    return dataclasses.replace(self.load_testdata(dummy_data_dict),
                               inputs=inputs,
                               platform=self.default_jax_backend())

  def load_testdata(self, testdata_dict: dict[str, Any]) -> CompatTestData:
    if testdata_dict["testdata_version"] == CURRENT_TESTDATA_VERSION:
      return CompatTestData(**testdata_dict)
    else:
      raise NotImplementedError("testdata_version not recognized: " +
                                testdata_dict["testdata_version"])

  def load_testdata_nested(self, testdata_nest) -> Iterable[CompatTestData]:
    # Load all the CompatTestData in a Python nest.
    if isinstance(testdata_nest, dict) and "testdata_version" in testdata_nest:
      yield self.load_testdata(testdata_nest)
    elif isinstance(testdata_nest, dict):
      for e in testdata_nest.values():
        yield from self.load_testdata_nested(e)
    elif isinstance(testdata_nest, list):
      for e in testdata_nest:
        yield from self.load_testdata_nested(e)
    else:
      assert False, testdata_nest

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

  def run_current(self, func: Callable, data: CompatTestData):
    """Lowers and runs the test function at the current JAX version."""
    return jax.jit(func)(*data.inputs)

  def serialize(self,
                func: Callable, data: CompatTestData, *,
                polymorphic_shapes: Sequence[str] | None = None,
                allow_unstable_custom_call_targets: Sequence[str] = ()
                ) -> tuple[bytes, str, int, int]:
    """Serializes the test function.

    Args:
      func: the function to serialize
      polymorphic_shapes: the polymorphic_shapes to use for serialization
      allow_unstable_custom_call_targets: whether to allow additional
        custom call targets besides those known as stable.

    Returns: a tuple with the (a) serialization, (b) the module contents as
      a string (for debugging), (c) the module serialization version,
      (d) the number of devices for which the module was serialized.
    """
    # Use the native exporter, to make sure we get the proper serialization.
    args_specs = export.symbolic_args_specs(data.inputs, polymorphic_shapes)
    exported = export.export(
      jax.jit(func),
      lowering_platforms=(self.default_jax_backend(),),
      disabled_checks=tuple(
        export.DisabledSafetyCheck.custom_call(target)
        for target in allow_unstable_custom_call_targets)
    )(*args_specs)

    module_str = str(exported.mlir_module())
    serialized = exported.mlir_module_serialized
    module_version = exported.mlir_module_serialization_version
    nr_devices = exported.nr_devices
    return serialized, module_str, module_version, nr_devices

  def run_serialized(self, data: CompatTestData,
                     polymorphic_shapes: Sequence[str] | None = None):
    args_specs = export.symbolic_args_specs(data.inputs, polymorphic_shapes)
    def ndarray_to_aval(a: np.ndarray) -> core.ShapedArray:
      return core.ShapedArray(a.shape, a.dtype)
    in_avals_tree = tree_util.tree_map(ndarray_to_aval, args_specs)
    # TODO: we ought to ensure that out_avals are polymorphic if need be. We
    # could either save the in/out_avals (but we need to first implement that
    # support in export), or we can just re-use them from the current
    # exported.
    out_avals_tree = tree_util.tree_map(ndarray_to_aval, data.expected_outputs)
    # in_tree must be for (args, kwargs)
    in_avals, in_tree = tree_util.tree_flatten((in_avals_tree, {}))
    out_avals, out_tree = tree_util.tree_flatten(out_avals_tree)
    def _get_vjp(_):
      assert False  # We do not have and do not need VJP

    exported = export.Exported(
        fun_name="run_serialized",
        in_tree=in_tree,
        in_avals=tuple(in_avals),
        out_tree=out_tree,
        out_avals=tuple(out_avals),
        in_shardings=(None,) * len(in_avals),
        out_shardings=(None,) * len(out_avals),
        lowering_platforms=(data.platform,),
        ordered_effects=(),
        unordered_effects=(),
        disabled_safety_checks=(),
        mlir_module_serialized=data.mlir_module_serialized,
        mlir_module_serialization_version=data.xla_call_module_version,
        nr_devices=data.nr_devices,
        module_kept_var_idx=tuple(range(len(in_avals))),
        uses_shape_polymorphism=any(not core.is_constant_shape(a.shape)
                                    for a in in_avals),
      _get_vjp=_get_vjp)

      # We use pjit in case there are shardings in the exported module.
    return pjit.pjit(export.call_exported(exported))(*data.inputs)
