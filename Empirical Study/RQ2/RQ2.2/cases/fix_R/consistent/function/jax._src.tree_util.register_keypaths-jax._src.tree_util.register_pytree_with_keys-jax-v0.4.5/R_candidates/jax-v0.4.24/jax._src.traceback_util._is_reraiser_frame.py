def _is_reraiser_frame(f: traceback.FrameSummary) -> bool:
  return (f.filename == __file__ and
          f.name == 'reraise_with_filtered_traceback')
