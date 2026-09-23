class _BackendSpecificTranslationsAdapter(defaultdict):
  def __missing__(self, key):
    translation_tables = [_backend_specific_translations[p]
                          for p in xb.expand_platform_alias(key)]
    ret = self[key] = _TranslationRuleAdapter(
        translation_tables, _wrap_old_translation)
    return ret
