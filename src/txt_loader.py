def load_txt(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text