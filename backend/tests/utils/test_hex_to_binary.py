from backend.util.hexbinary import hex_to_binary


def test_hex_to_binary():
    hex_string = "012"
    assert hex_to_binary(hex_string) == '000000010010'


def test_hex_to_binary_2():
    hex_string = "3456789"
    assert hex_to_binary(hex_string) == '0011010001010110011110001001'


def test_hex_to_binary_3():
    hex_string = "abcdef"
    assert hex_to_binary(hex_string) == '101010111100110111101111'