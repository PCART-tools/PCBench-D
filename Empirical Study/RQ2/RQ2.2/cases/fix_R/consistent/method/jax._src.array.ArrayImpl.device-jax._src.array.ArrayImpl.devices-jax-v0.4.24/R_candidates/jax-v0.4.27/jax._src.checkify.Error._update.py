  def _update(self, effect_type: ErrorEffect, pred, code, metadata, payload):
    new_errs = {**self._pred, **{effect_type: pred}}  # type: ignore
    new_codes = {**self._code, **{effect_type: code}}  # type: ignore
    new_payload = {**self._payload, **{effect_type: payload}}  # type: ignore
    new_metadata = {**self._metadata, **metadata}
    return Error(new_errs, new_codes, new_metadata, new_payload)
