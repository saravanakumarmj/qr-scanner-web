def build_two_label_zpl(
    left_qr: str,
    right_qr: str | None = None,
) -> str:
    """Build ZPL for two labels, with optional right label."""

    if not left_qr:
        raise ValueError("Left QR value is required.")

    zpl = f"""^XA
^PW400
^LL200
^LH0,25

^FO0,2
^A0N,20,20
^FB200,1,0,C
^FD{left_qr}^FS

^FO15,22
^BQN,2,7
^FDLA,{left_qr}^FS
"""

    if right_qr:
        zpl += f"""
^FO200,2
^A0N,20,20
^FB200,1,0,C
^FD{right_qr}^FS

^FO215,22
^BQN,2,7
^FDLA,{right_qr}^FS
"""

    zpl += """
^XZ
"""

    return zpl