def summarize(source_info: SourceInfo, num_frames=1) -> str:
  frames = itertools.islice(user_frames(source_info), num_frames)
  frame_strs = [f"{frame.file_name}:{frame.line_num} ({frame.function_name})"
                if frame else "unknown" for frame in frames]
  return '\n'.join(reversed(frame_strs))
