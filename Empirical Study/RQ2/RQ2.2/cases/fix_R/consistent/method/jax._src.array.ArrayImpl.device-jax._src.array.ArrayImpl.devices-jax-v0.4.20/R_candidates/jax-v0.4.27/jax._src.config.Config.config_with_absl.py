  def config_with_absl(self):
    """Registers absl flags for the JAX configs.

    E.g., for each JAX config defined using define_bool_state(), this method
    registers an absl boolean flag, with the same name.

    This is the recommended method to call if you use `app.run(main)` and you
    need JAX flags.  Example:

    ```python
    from absl import app
    import jax
    ...

    if __name__ == '__main__':
      jax.config.config_with_absl()
      app.run(main)
    ```

    """
    import absl.flags as absl_FLAGS  # noqa: F401  # pytype: disable=import-error
    from absl import app, flags as absl_flags  # pytype: disable=import-error

    self.use_absl = True
    self.absl_flags = absl_flags
    absl_defs = { bool: absl_flags.DEFINE_bool,
                  int:  absl_flags.DEFINE_integer,
                  float: absl_flags.DEFINE_float,
                  str:  absl_flags.DEFINE_string,
                  'enum': absl_flags.DEFINE_enum }

    for name, (flag_type, meta_args, meta_kwargs) in self.meta.items():
      holder = self._value_holders[name]
      absl_defs[flag_type](name, holder.value, *meta_args, **meta_kwargs)
    app.call_after_init(lambda: self.complete_absl_config(absl_flags))
