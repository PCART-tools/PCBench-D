    def _add_to_previous_pixels(self, value: bytes | bytearray) -> None:
        self._previous_pixel = value

        r, g, b, a = value
        hash_value = (r * 3 + g * 5 + b * 7 + a * 11) % 64
        self._previously_seen_pixels[hash_value] = value
