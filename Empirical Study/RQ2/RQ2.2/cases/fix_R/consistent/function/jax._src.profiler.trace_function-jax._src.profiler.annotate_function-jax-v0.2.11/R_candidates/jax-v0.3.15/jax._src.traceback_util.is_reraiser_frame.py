def is_reraiser_frame(f):
  return (f.filename == __file__ and
          f.name == 'reraise_with_filtered_traceback')
