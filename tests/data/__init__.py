from pathlib import Path

DATA_DIR = Path(__file__).parent


def read_data_file(name: str) -> str:
    with open(DATA_DIR / name) as file:
        return file.read()