def main() -> None:

    upgrader_list = generate_upgraders_bytecode()
    sorted_upgrader_list = sort_upgrader(upgrader_list)
    for up in sorted_upgrader_list:
        print("after sort upgrader : ", next(iter(up)))

    pytorch_dir = Path(__file__).resolve().parents[3]
    upgrader_path = pytorch_dir / "torch" / "csrc" / "jit" / "mobile"
    write_cpp(str(upgrader_path), sorted_upgrader_list)
