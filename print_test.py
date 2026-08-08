import win32print

PRINTER_NAME = "Zebra ZD230 printer"

LEFT_TEXT = "175I0G"
RIGHT_TEXT = "175I0S"

zpl = f"""
^XA
^PW400
^LL200
^LH0,25

^A0N,20,20

^FO0,2
^FB200,1,0,C
^FD{LEFT_TEXT}^FS

^FO200,2
^FB200,1,0,C
^FD{RIGHT_TEXT}^FS

^FO15,22
^BQN,2,7
^FDLA,{LEFT_TEXT}^FS

^FO215,22
^BQN,2,7
^FDLA,{RIGHT_TEXT}^FS

^XZ
"""

printer = win32print.OpenPrinter(PRINTER_NAME)

try:
    win32print.StartDocPrinter(printer, 1, ("QR Label", None, "RAW"))
    win32print.StartPagePrinter(printer)

    win32print.WritePrinter(printer, zpl.encode("utf-8"))

    win32print.EndPagePrinter(printer)
    win32print.EndDocPrinter(printer)

    print("Label printed successfully.")

finally:
    win32print.ClosePrinter(printer)