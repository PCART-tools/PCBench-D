    @staticmethod
    def _verify_bytes_written(bytes_written: int | None, expected: int) -> None:
        if bytes_written is not None and bytes_written != expected:
            msg = f"wrote only {bytes_written} bytes but wanted {expected}"
            raise RuntimeError(msg)
