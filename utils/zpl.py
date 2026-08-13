"""Zebra ZPL generation utilities."""

from __future__ import annotations


def build_two_label_zpl(left_qr: str, right_qr: str) -> str:
    """Build ZPL for two QR labels printed side-by-side."""

    if not left_qr:
        raise ValueError("Left QR value is required.")

    if not right_qr:
        raise ValueError("Right QR value is required.")

    return f"""^XA
^PW400
^LL200
^LH0,25

^FO0,2
^A0N,20,20
^FB200,1,0,C
^FD{left_qr}^FS

^FO200,2
^A0N,20,20
^FB200,1,0,C
^FD{right_qr}^FS

^FO15,22
^BQN,2,7
^FDLA,{left_qr}^FS

^FO215,22
^BQN,2,7
^FDLA,{right_qr}^FS

^XZ
"""
