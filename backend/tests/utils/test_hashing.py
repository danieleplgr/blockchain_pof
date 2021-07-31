from backend.util.hashing import get_block_hash


def test_fixed_sha256_hashing():
    """
    Test that a fixed pre-defined input produce always the expected sha256 hash
    """
    assert get_block_hash('foo') == 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'



def test_crypto_hash_order_not_matter():
    """
    Tests that different input order don't change the hash
    """
    assert get_block_hash(1, "two", {"a": 2}) == get_block_hash( {"a": 2}, "two", 1)

