"""Base36 encoding and decoding utilities."""

from __future__ import annotations


_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_base36(value: int) -> str:
    """Convert a non-negative integer to uppercase Base36."""

    if value < 0:
        raise ValueError("Base36 value cannot be negative.")

    if value == 0:
        return "0"

    result = ""

    while value:
        value, remainder = divmod(value, 36)
        result = _ALPHABET[remainder] + result

    return result


def decode_base36(value: str) -> int:
    """Convert a Base36 string back to an integer."""

    value = value.strip().upper()

    if not value:
        raise ValueError("Base36 value cannot be empty.")

    result = 0

    for character in value:
        if character not in _ALPHABET:
            raise ValueError(f"Invalid Base36 character: {character}")

        result = result * 36 + _ALPHABET.index(character)

    return result