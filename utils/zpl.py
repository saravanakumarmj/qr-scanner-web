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



def build_four_label_zpl(qr_values: list[str]) -> str:
    """Build ZPL for up to four 25x25 mm QR labels in one row."""

    if not qr_values:
        raise ValueError("At least one QR value is required.")

    if len(qr_values) > 4:
        raise ValueError("Maximum four QR values are allowed per row.")

    zpl = """^XA
^PW800
^LL200
^LH0,25
"""

    for index, qr_value in enumerate(qr_values):
        if not qr_value:
            raise ValueError("QR value cannot be empty.")

        x = index * 200

        zpl += f"""
^FO{x},2
^A0N,20,20
^FB200,1,0,C
^FD{qr_value}^FS

^FO{x + 15},22
^BQN,2,7
^FDLA,{qr_value}^FS
"""

    zpl += """
^XZ
"""

    return zpl
