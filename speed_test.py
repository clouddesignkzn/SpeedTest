#!/usr/bin/env python3
"""Sequentially measure download speed for a URL."""

from __future__ import annotations

import argparse
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


REQUEST_COUNT = 10
CHUNK_SIZE = 1024 * 1024
TIMEOUT_SECONDS = 60


def download_once(url: str) -> tuple[float, int]:
    """Download the complete response and return (elapsed_seconds, bytes)."""
    request = Request(url, headers={"User-Agent": "internet-speed-test/1.0"})
    started_at = time.perf_counter()
    total_bytes = 0

    with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            total_bytes += len(chunk)

    return time.perf_counter() - started_at, total_bytes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a URL 10 times sequentially and measure the speed."
    )
    parser.add_argument("url", help="HTTP(S) URL to download")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    parsed_url = urlparse(args.url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        print("Ошибка: укажите корректный HTTP(S)-адрес.", file=sys.stderr)
        return 2

    elapsed_times: list[float] = []
    total_bytes = 0

    print(f"Запрашиваю {args.url} — {REQUEST_COUNT} раз(а) последовательно...")
    try:
        for request_number in range(1, REQUEST_COUNT + 1):
            elapsed, downloaded_bytes = download_once(args.url)
            elapsed_times.append(elapsed)
            total_bytes += downloaded_bytes
            print(
                f"Запрос {request_number}/{REQUEST_COUNT}: "
                f"{downloaded_bytes / 1_000_000:.2f} MB за {elapsed:.3f} с"
            )
    except (HTTPError, URLError, TimeoutError, OSError) as error:
        print(f"Ошибка при выполнении запроса: {error}", file=sys.stderr)
        return 1

    total_elapsed = sum(elapsed_times)
    average_elapsed = total_elapsed / REQUEST_COUNT
    speed_bytes_per_second = total_bytes / total_elapsed if total_elapsed else 0.0
    speed_megabits_per_second = speed_bytes_per_second * 8 / 1_000_000

    print("\nИтоги скачивания:")
    print(f"Среднее время запроса: {average_elapsed:.3f} с")
    print(f"Объём скачанных данных: {total_bytes / 1_000_000:.2f} MB")
    print(f"Скорость скачивания (MB/s): {speed_bytes_per_second / 1_000_000:.2f}")
    print(f"Скорость скачивания (Mbit/s): {speed_megabits_per_second:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
