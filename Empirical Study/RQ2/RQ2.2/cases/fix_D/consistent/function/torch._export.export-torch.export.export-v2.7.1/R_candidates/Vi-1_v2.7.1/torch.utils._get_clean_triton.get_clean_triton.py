def get_clean_triton(
    input_path: Path, output_path: Path = Path("triton_only_repro.py")
):
    """Run experiments and output results to file

    Args:
        input_path (Optional[Path]): Path to inductor generated output codede
        output_path (Optional[Path]): Path to write out the new python file
    """
    return process_file(str(input_path), str(output_path))
