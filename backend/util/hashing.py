import hashlib, json


def get_block_hash(*args):
    """
    Returns a unique hash sha256 from the gives args 
    """
    stringified_sorted_args_list = sorted(map(lambda data: json.dumps(data), args))
    data_bytes = "".join(stringified_sorted_args_list).encode("utf-8")
    return hashlib.sha256(data_bytes).hexdigest()
