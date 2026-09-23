class JaxTestCase(parameterized.TestCase):
  """Base class for JAX tests including numerical checks and boilerplate."""
  _default_config = {
    'jax_enable_checks': True,
    'jax_enable_key_reuse_checks': True,
    'jax_numpy_dtype_promotion': 'strict',
    'jax_numpy_rank_promotion': 'raise',
    'jax_traceback_filtering': 'off',
    'jax_legacy_prng_key': 'error',
  }

  _compilation_cache_exit_stack: ExitStack | None = None

  # TODO(mattjj): this obscures the error messages from failures, figure out how
  # to re-enable it
  # def tearDown(self) -> None:
  #   assert core.reset_trace_state()

  def setUp(self):
    super().setUp()
    self._original_config = {}
    for key, value in self._default_config.items():
      self._original_config[key] = config._read(key)
      config.update(key, value)

    # We use the adler32 hash for two reasons.
    # a) it is deterministic run to run, unlike hash() which is randomized.
    # b) it returns values in int32 range, which RandomState requires.
    self._rng = npr.RandomState(zlib.adler32(self._testMethodName.encode()))

  def tearDown(self):
    for key, value in self._original_config.items():
      config.update(key, value)
    super().tearDown()

  @classmethod
  def setUpClass(cls):
    if TEST_WITH_PERSISTENT_COMPILATION_CACHE.value:
      cls._compilation_cache_exit_stack = ExitStack()
      stack = cls._compilation_cache_exit_stack
      stack.enter_context(config.enable_compilation_cache(True))
      stack.enter_context(config.raise_persistent_cache_errors(True))
      stack.enter_context(config.persistent_cache_min_compile_time_secs(0))
      stack.enter_context(config.persistent_cache_min_entry_size_bytes(0))

      tmp_dir = stack.enter_context(tempfile.TemporaryDirectory())
      compilation_cache.set_cache_dir(tmp_dir)
      stack.callback(lambda: compilation_cache.reset_cache())

  @classmethod
  def tearDownClass(cls):
    if TEST_WITH_PERSISTENT_COMPILATION_CACHE.value:
      cls._compilation_cache_exit_stack.close()

  def rng(self):
    return self._rng

  def assertArraysEqual(self, x, y, *, check_dtypes=True, err_msg='',
                        allow_object_dtype=False, verbose=True):
    """Assert that x and y arrays are exactly equal."""
    if check_dtypes:
      self.assertDtypesMatch(x, y)
    x = np.asarray(x)
    y = np.asarray(y)

    if (not allow_object_dtype) and (x.dtype == object or y.dtype == object):
      # See https://github.com/google/jax/issues/17867
      raise TypeError(
        "assertArraysEqual may be poorly behaved when np.asarray casts to dtype=object. "
        "If comparing PRNG keys, consider random_test.KeyArrayTest.assertKeysEqual. "
        "If comparing collections of arrays, consider using assertAllClose. "
        "To let this test proceed anyway, pass allow_object_dtype=True.")

    # Work around https://github.com/numpy/numpy/issues/18992
    with np.errstate(over='ignore'):
      np.testing.assert_array_equal(x, y, err_msg=err_msg,
                                    verbose=verbose)

  def assertArraysAllClose(self, x, y, *, check_dtypes=True, atol=None,
                           rtol=None, err_msg=''):
    """Assert that x and y are close (up to numerical tolerances)."""
    self.assertEqual(x.shape, y.shape)
    atol = max(tolerance(_dtype(x), atol), tolerance(_dtype(y), atol))
    rtol = max(tolerance(_dtype(x), rtol), tolerance(_dtype(y), rtol))

    _assert_numpy_allclose(x, y, atol=atol, rtol=rtol, err_msg=err_msg)

    if check_dtypes:
      self.assertDtypesMatch(x, y)

  def assertDtypesMatch(self, x, y, *, canonicalize_dtypes=True):
    if not config.enable_x64.value and canonicalize_dtypes:
      self.assertEqual(_dtypes.canonicalize_dtype(_dtype(x), allow_extended_dtype=True),
                       _dtypes.canonicalize_dtype(_dtype(y), allow_extended_dtype=True))
    else:
      self.assertEqual(_dtype(x), _dtype(y))

  def assertAllClose(self, x, y, *, check_dtypes=True, atol=None, rtol=None,
                     canonicalize_dtypes=True, err_msg=''):
    """Assert that x and y, either arrays or nested tuples/lists, are close."""
    if isinstance(x, dict):
      self.assertIsInstance(y, dict)
      self.assertEqual(set(x.keys()), set(y.keys()))
      for k in x.keys():
        self.assertAllClose(x[k], y[k], check_dtypes=check_dtypes, atol=atol,
                            rtol=rtol, canonicalize_dtypes=canonicalize_dtypes,
                            err_msg=err_msg)
    elif is_sequence(x) and not hasattr(x, '__array__'):
      self.assertTrue(is_sequence(y) and not hasattr(y, '__array__'))
      self.assertEqual(len(x), len(y))
      for x_elt, y_elt in zip(x, y):
        self.assertAllClose(x_elt, y_elt, check_dtypes=check_dtypes, atol=atol,
                            rtol=rtol, canonicalize_dtypes=canonicalize_dtypes,
                            err_msg=err_msg)
    elif hasattr(x, '__array__') or np.isscalar(x):
      self.assertTrue(hasattr(y, '__array__') or np.isscalar(y))
      if check_dtypes:
        self.assertDtypesMatch(x, y, canonicalize_dtypes=canonicalize_dtypes)
      x = np.asarray(x)
      y = np.asarray(y)
      self.assertArraysAllClose(x, y, check_dtypes=False, atol=atol, rtol=rtol,
                                err_msg=err_msg)
    elif x == y:
      return
    else:
      raise TypeError((type(x), type(y)))

  def assertMultiLineStrippedEqual(self, expected, what):
    """Asserts two strings are equal, after dedenting and stripping each line."""
    expected = textwrap.dedent(expected)
    what = textwrap.dedent(what)
    ignore_space_re = re.compile(r'\s*\n\s*')
    expected_clean = re.sub(ignore_space_re, '\n', expected.strip())
    what_clean = re.sub(ignore_space_re, '\n', what.strip())
    if what_clean != expected_clean:
      # Print it so we can copy-and-paste it into the test
      print(f"Found\n{what}\n")
    self.assertMultiLineEqual(expected_clean, what_clean,
                              msg=f"Found\n{what}\nExpecting\n{expected}")

  @contextmanager
  def assertNoWarnings(self):
    with warnings.catch_warnings():
      warnings.simplefilter("error")
      yield

  def _CompileAndCheck(self, fun, args_maker, *, check_dtypes=True, tol=None,
                       rtol=None, atol=None, check_cache_misses=True):
    """Helper method for running JAX compilation and allclose assertions."""
    args = args_maker()

    def wrapped_fun(*args):
      self.assertTrue(python_should_be_executing)
      return fun(*args)

    python_should_be_executing = True
    python_ans = fun(*args)

    python_shapes = tree_map(lambda x: np.shape(x), python_ans)
    np_shapes = tree_map(lambda x: np.shape(np.asarray(x)), python_ans)
    self.assertEqual(python_shapes, np_shapes)

    cache_misses = dispatch.xla_primitive_callable.cache_info().misses
    python_ans = fun(*args)
    if check_cache_misses:
      self.assertEqual(
          cache_misses, dispatch.xla_primitive_callable.cache_info().misses,
          "Compilation detected during second call of {} in op-by-op "
          "mode.".format(fun))

    cfun = api.jit(wrapped_fun)
    python_should_be_executing = True
    monitored_ans = cfun(*args)

    python_should_be_executing = False
    compiled_ans = cfun(*args)

    self.assertAllClose(python_ans, monitored_ans, check_dtypes=check_dtypes,
                        atol=atol or tol, rtol=rtol or tol)
    self.assertAllClose(python_ans, compiled_ans, check_dtypes=check_dtypes,
                        atol=atol or tol, rtol=rtol or tol)

    args = args_maker()

    python_should_be_executing = True
    python_ans = fun(*args)

    python_should_be_executing = False
    compiled_ans = cfun(*args)

    self.assertAllClose(python_ans, compiled_ans, check_dtypes=check_dtypes,
                        atol=atol or tol, rtol=rtol or tol)

  def _CheckAgainstNumpy(self, numpy_reference_op, lax_op, args_maker,
                         check_dtypes=True, tol=None, atol=None, rtol=None,
                         canonicalize_dtypes=True):
    args = args_maker()
    lax_ans = lax_op(*args)
    numpy_ans = numpy_reference_op(*args)
    self.assertAllClose(numpy_ans, lax_ans, check_dtypes=check_dtypes,
                        atol=atol or tol, rtol=rtol or tol,
                        canonicalize_dtypes=canonicalize_dtypes)
