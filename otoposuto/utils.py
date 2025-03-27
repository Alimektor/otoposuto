import hashlib
import inspect

from otoposuto.colors import green_color, reset_color, yellow_color


def m_print(message):
    caller_frame = inspect.currentframe().f_back
    caller_globals = caller_frame.f_globals
    full_module_name = caller_globals.get("__name__", "Unknown").upper()
    module_name = full_module_name.split(".")[-1]
    print(f"{green_color}[{module_name}]{yellow_color} {message}{reset_color}")


def m_input(message):
    caller_frame = inspect.currentframe().f_back
    caller_globals = caller_frame.f_globals
    full_module_name = caller_globals.get("__name__", "Unknown").upper()
    module_name = full_module_name.split(".")[-1]
    return input(
        f"{green_color}[{module_name}]{yellow_color} {message} {green_color}>>> {reset_color}"
    )


def get_file_hash(file_path, algorithm="sha256"):
    try:
        hash_func = getattr(hashlib, algorithm)()
    except AttributeError:
        raise ValueError(f"Unsupported hashing algorithm: {algorithm}")
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hash_func.update(chunk)
    return hash_func.hexdigest()
