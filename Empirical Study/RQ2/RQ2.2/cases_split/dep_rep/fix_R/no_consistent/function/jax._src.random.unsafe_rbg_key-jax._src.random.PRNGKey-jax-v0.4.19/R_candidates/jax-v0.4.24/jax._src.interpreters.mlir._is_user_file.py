def _is_user_file(ctx: ModuleContext, file_name: str) -> bool:
  if file_name in ctx.traceback_caches.is_user_file_cache:
    return ctx.traceback_caches.is_user_file_cache[file_name]

  result = source_info_util.is_user_filename(file_name)
  ctx.traceback_caches.is_user_file_cache[file_name] = result
  return result
