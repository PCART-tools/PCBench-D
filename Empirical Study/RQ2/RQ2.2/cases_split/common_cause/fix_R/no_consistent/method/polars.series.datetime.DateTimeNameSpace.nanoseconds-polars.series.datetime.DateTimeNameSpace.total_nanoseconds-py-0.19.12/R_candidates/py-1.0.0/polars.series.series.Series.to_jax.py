    @unstable()
    def to_jax(self, device: jax.Device | str | None = None) -> jax.Array:
        """
        Convert this Series to a Jax Array.

        .. versionadded:: 0.20.27

        .. warning::
            This functionality is currently considered **unstable**. It may be
            changed at any point without it being considered a breaking change.

        Parameters
        ----------
        device
            Specify the jax `Device` on which the array will be created; can provide
            a string (such as "cpu", "gpu", or "tpu") in which case the device is
            retrieved as `jax.devices(string)[0]`. For more specific control you
            can supply the instantiated `Device` directly. If None, arrays are
            created on the default device.

        Examples
        --------
        >>> s = pl.Series("x", [10.5, 0.0, -10.0, 5.5])
        >>> s.to_jax()
        Array([ 10.5,   0. , -10. ,   5.5], dtype=float32)
        """
        jx = import_optional(
            "jax",
            install_message="Please see `https://jax.readthedocs.io/en/latest/installation.html` "
            "for specific installation recommendations for the Jax package",
        )
        if isinstance(device, str):
            device = jx.devices(device)[0]
        if (
            jx.config.jax_enable_x64
            or bool(int(os.environ.get("JAX_ENABLE_X64", "0")))
            or self.dtype not in {Float64, Int64, UInt64}
        ):
            srs = self
        else:
            single_precision = {Float64: Float32, Int64: Int32, UInt64: UInt32}
            srs = self.cast(single_precision[self.dtype])  # type: ignore[index]

        with nullcontext() if device is None else jx.default_device(device):
            return jx.numpy.asarray(
                # note: jax arrays are immutable, so can avoid a copy (vs torch)
                a=srs.to_numpy(writable=False),
                order="K",
            )
