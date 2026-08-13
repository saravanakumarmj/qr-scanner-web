import win32file
import pywintypes

port = r"\\.\USB002"

try:
    handle = win32file.CreateFile(
        port,
        win32file.GENERIC_READ | win32file.GENERIC_WRITE,
        0,
        None,
        win32file.OPEN_EXISTING,
        0,
        None,
    )

    print("USB port: CONNECTED")

    win32file.CloseHandle(handle)

except pywintypes.error as e:
    print("USB port: NOT CONNECTED")
    print("Error:", e)