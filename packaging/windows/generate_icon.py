from __future__ import annotations

from pathlib import Path
import struct


def generate_icon(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    w = h = 16
    icon_dir = struct.pack('<HHH', 0, 1, 1)
    bytes_in_res = 40 + w * h * 4 + ((w + 31) // 32 * 4) * h
    entry = struct.pack('<BBBBHHII', w, h, 0, 0, 1, 32, bytes_in_res, 22)
    header = struct.pack('<IIIHHIIIIII', 40, w, h * 2, 1, 32, 0, w * h * 4, 0, 0, 0, 0)
    pixels = bytes([0, 128, 0, 255]) * (w * h)
    mask = bytes(((w + 31) // 32 * 4) * h)

    path.write_bytes(icon_dir + entry + header + pixels + mask)


if __name__ == '__main__':
    repo_root = Path(__file__).resolve().parents[2]
    generate_icon(repo_root / 'client' / 'assets' / 'icon.ico')
