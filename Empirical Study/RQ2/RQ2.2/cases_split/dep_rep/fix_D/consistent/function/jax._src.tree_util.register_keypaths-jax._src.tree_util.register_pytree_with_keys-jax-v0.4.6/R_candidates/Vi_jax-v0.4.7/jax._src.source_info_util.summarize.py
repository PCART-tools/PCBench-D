def summarize(source_info: SourceInfo, num_frames=1) -> str:
  frames = itertools.islice(user_frames(source_info), num_frames)
  frame_strs = [_summarize_frame(frame) if frame else "unknown"
                for frame in frames]
  return '\n'.join(reversed(frame_strs))
