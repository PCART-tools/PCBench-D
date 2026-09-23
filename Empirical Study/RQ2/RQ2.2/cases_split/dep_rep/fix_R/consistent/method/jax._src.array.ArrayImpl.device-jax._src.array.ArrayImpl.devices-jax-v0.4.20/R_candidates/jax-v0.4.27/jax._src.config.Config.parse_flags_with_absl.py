  def parse_flags_with_absl(self):
    """Parses command-line args that start with --jax.

    This method should be used only by advanced users. Most users should use
    :meth:`config_with_absl` instead.

    This method has serious limitations: e.g., although it parses only the
    --jax* command-line args, it runs the validators of all registered absl
    flags, even non-JAX ones that have not been set yet; as such, for the
    non-JAX flags, the validators run on the default flag values, not on the
    values indicated by the command-line args.
    """
    global already_configured_with_absl
    if not already_configured_with_absl:
      # Extract just the --jax... flags (before the first --) from argv. In some
      # environments (e.g. ipython/colab) argv might be a mess of things
      # parseable by absl and other junk.
      jax_argv = itertools.takewhile(lambda a: a != '--', sys.argv)
      jax_argv = ['', *(a for a in jax_argv if a.startswith('--jax'))]

      import absl.flags  # pytype: disable=import-error
      self.config_with_absl()
      absl.flags.FLAGS(jax_argv, known_only=True)
      self.complete_absl_config(absl.flags)
      already_configured_with_absl = True
