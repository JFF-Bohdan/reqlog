import ksuid


def get_string_ksuid():
    return str(ksuid.ksuid())


def get_base62_ksuid():
    return ksuid.ksuid().toBase62()
