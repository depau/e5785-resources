#!/system/bin/env micropython
# -*- coding: utf-8 -*-

import sys
import time
import ffi

O_RDWR = 0o000002
O_NOCTTY = 0o000400
O_DSYNC = 0o001000


class libc:
    _lib = ffi.open("libc.so")

    open = _lib.func("i", "open", "si")  # int open(const char*, int)
    read = _lib.func("i", "read", "ipi")  # int read(int, void*, size_t)
    write = _lib.func("i", "write", "ipL")  # ssize_t write(int,const void*,size_t)
    close = _lib.func("i", "close", "i")  # int close(int)

    perror = _lib.func("v", "perror", "s")  # void perror(const char*)


def run_at_command(cmd: str, port=b"/dev/appvcom1") -> str | None:
    if not cmd.endswith("\r"):
        cmd = cmd + "\r"

    fd = libc.open(port, O_RDWR | O_NOCTTY | O_DSYNC)
    if fd < 0:
        libc.perror(f"failed to open AT port '{port}'".encode("ascii"))
        return None

    try:
        # AT^CURC=0
        libc.write(fd, b"AT^CURC=0\r", 10)
        time.sleep_ms(100)

        # dummy read (like FULL 0x10000 read in original)
        buf = bytearray(65536)
        libc.read(fd, buf, len(buf))

        # write user command
        libc.write(fd, cmd.encode(), len(cmd))
        time.sleep_ms(50)

        # read first byte
        first = bytearray(1)
        r1 = libc.read(fd, first, 1)

        # read the bulk of response (0x2000 → 8192 bytes)
        rest = bytearray(8192)
        r2 = libc.read(fd, rest, len(rest))

        # AT^CURC=1
        libc.write(fd, b"AT^CURC=1\r", 10)
        time.sleep_ms(50)

    finally:
        libc.close(fd)

    # construct output like v13 + v14[...] with dropped last byte
    data = bytes(first[: max(r1, 0)]) + bytes(rest[: max(r2 - 1, 0)])
    return data.decode("ascii", "ignore") if data else ""


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <AT-CMD>")
        sys.exit(1)

    cmd = sys.argv[1]

    if not cmd.startswith("AT"):
        print("Command must begin with AT")
        sys.exit(1)

    resp = run_at_command(cmd)
    print(resp or "(no response)")


if __name__ == "__main__":
    main()
