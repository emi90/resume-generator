import os



def get_extension(filename: str | None) -> str:
    if not filename:
        return ""
    return os.path.splitext(filename)[1].lower()
