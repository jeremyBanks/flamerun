#!/usr/bin/env python3
import sys
import json
from os.path import expanduser as user_path
from pprint import pprint
from subprocess import PIPE, Popen as popen


def main():
    videos_response, _ = popen(
        [
            "youtube-dl",
            "-j",
            "--flat-playlist",
            "https://www.youtube.com/playlist?list=PLCotwPB4IR4hQE8zSt6EPC5Jrt1rdN1sL",
        ],
        stdout=PIPE,
    ).communicate()

    video_ids = [
        json.loads(line)["id"]
        for line in filter(bool, videos_response.decode("utf-8").split("\n"))
    ]

    runs_output, _ = popen(
        [
            user_path("~/.cargo/bin/cargo"),
            "+nightly",
            "run",
            "--",
            "--max-age-days=360",
        ],
        env={"RUST_BACKTRACE": "1", "RUST_LOG": "flamerun=warn"},
        stdout=PIPE,
    ).communicate()

    run_lines = list(
        filter(
            lambda l: l and "szwagier" in l.lower(),
            runs_output.decode("utf-8").split("\n"),
        )
    )

    for line in run_lines:
        for video_id in video_ids:
            if video_id in line:
                break
        else:
            print(f"not in playlist: {line}")

    for video_id in video_ids:
        for line in run_lines:
            if video_id in line:
                break
        else:
            print(f"not on speedrun: https://yt-timer-1806.glitch.me/?v={video_id}")


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
