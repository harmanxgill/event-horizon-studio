from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections.abc import Iterator
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


PIECE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PIECE_DIR.parents[1]
EXPERIMENTS = PIECE_DIR / "experiments"
DEFAULT_OUTPUT = PROJECT_ROOT / "gallery" / "001_THE_LAST_ORBIT_TIMELAPSE.mp4"
FINAL_EXPERIMENT = EXPERIMENTS / "v030_final_tone.py"

VERSION_RENDER = re.compile(r"^v(\d{3})_([a-z0-9_]+)\.png$")
DIAGNOSTIC_SUFFIXES = ("_series", "_signed")
LABEL_FONTS = ("/System/Library/Fonts/SFNSMono.ttf", "/System/Library/Fonts/Menlo.ttc")


def version_renders(directory: Path = EXPERIMENTS) -> list[tuple[int, str, Path]]:
    # one still per version; phase series and signed diagnostics are not part of the sequence
    renders: dict[int, tuple[int, str, Path]] = {}
    for path in sorted(directory.glob("v*.png")):
        match = VERSION_RENDER.match(path.name)
        if match is None or match.group(2).endswith(DIAGNOSTIC_SUFFIXES):
            continue
        number = int(match.group(1))
        renders[number] = (number, match.group(2).replace("_", " "), path)
    return [renders[number] for number in sorted(renders)]


def load_frame(path: Path, size: int) -> np.ndarray:
    image = Image.open(path).convert("RGB")
    if image.size != (size, size):
        image = image.resize((size, size), Image.LANCZOS)
    return np.asarray(image)


def label_font(size: int) -> ImageFont.ImageFont:
    for candidate in LABEL_FONTS:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def with_label(rgb: np.ndarray, text: str | None, opacity: float = 1.0) -> np.ndarray:
    if not text or opacity <= 0.0:
        return rgb
    size = rgb.shape[0]
    font = label_font(max(12, size // 48))
    mask = Image.new("L", (rgb.shape[1], size), 0)
    margin = size // 30
    ImageDraw.Draw(mask).text((margin, size - margin), text, font=font, fill=255, anchor="ls")
    alpha = np.asarray(mask, dtype=np.float64)[..., None] / 255.0 * float(opacity)
    ink = np.array([170.0, 160.0, 150.0])
    return np.round(rgb * (1.0 - alpha) + ink * alpha).astype(np.uint8)


def crossfade(start: np.ndarray, end: np.ndarray, frames: int) -> Iterator[np.ndarray]:
    for index in range(1, frames + 1):
        t = index / (frames + 1)
        weight = t * t * (3.0 - 2.0 * t)
        yield np.round(start * (1.0 - weight) + end * weight).astype(np.uint8)


def load_final_experiment():
    spec = importlib.util.spec_from_file_location("last_orbit_v030_timelapse", FINAL_EXPERIMENT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def evolution_frames(
    size: int,
    fps: int,
    hold: float,
    fade: float,
    final_hold: float,
    labels: bool,
) -> Iterator[np.ndarray]:
    renders = version_renders()
    if not renders:
        raise FileNotFoundError(f"no version renders in {EXPERIMENTS}")

    hold_frames = max(1, round(hold * fps))
    fade_frames = max(0, round(fade * fps))
    previous = None
    for position, (number, name, path) in enumerate(renders):
        text = f"v{number:03d}  {name}" if labels else None
        frame = with_label(load_frame(path, size), text)
        if previous is not None:
            yield from crossfade(previous, frame, fade_frames)
        last = position == len(renders) - 1
        for _ in range(max(hold_frames, round(final_hold * fps)) if last else hold_frames):
            yield frame
        previous = frame


def orbit_frames(
    size: int,
    fps: int,
    seconds: float,
    labels: bool,
    final_name: str,
) -> Iterator[np.ndarray]:
    final = load_final_experiment()
    count = max(1, round(seconds * fps))
    label_fade = max(1, fps)
    for index in range(count):
        # the orbit starts at phase 0, the same image the evolution ends on, and closes the loop
        phase = 2.0 * np.pi * index / count
        rgb = final.v030_rgb(size, size, phase=phase, strip_rows=max(1, size // 4))
        opacity = max(0.0, 1.0 - index / label_fade) if labels else 0.0
        yield with_label(rgb, final_name, opacity)
        if (index + 1) % fps == 0:
            print(f"orbit {index + 1}/{count}", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render the v001-v030 timelapse of The Last Orbit.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--size", type=int, default=1080)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--hold", type=float, default=0.8, help="seconds each version is held")
    parser.add_argument("--fade", type=float, default=0.4, help="seconds of crossfade between versions")
    parser.add_argument("--final-hold", type=float, default=3.0, help="seconds v030 is held")
    parser.add_argument("--orbit-seconds", type=float, default=10.0, help="0 skips the closing orbit")
    parser.add_argument("--crf", type=int, default=16)
    parser.add_argument("--no-labels", action="store_true")
    return parser.parse_args()


def main() -> None:
    try:
        import imageio_ffmpeg
    except ImportError:
        sys.exit('video output needs imageio-ffmpeg: pip install -e ".[video]"')

    options = parse_args()
    if options.size % 2:
        sys.exit("size must be even for yuv420p video")
    labels = not options.no_labels
    options.output.parent.mkdir(parents=True, exist_ok=True)

    writer = imageio_ffmpeg.write_frames(
        str(options.output),
        (options.size, options.size),
        fps=options.fps,
        codec="libx264",
        pix_fmt_out="yuv420p",
        quality=None,
        macro_block_size=2,
        output_params=["-crf", str(options.crf), "-preset", "slow", "-movflags", "+faststart"],
    )
    writer.send(None)

    frames = 0
    for frame in evolution_frames(
        options.size, options.fps, options.hold, options.fade, options.final_hold, labels
    ):
        writer.send(np.ascontiguousarray(frame))
        frames += 1
    print(f"evolution: {frames} frames", flush=True)

    final_name = version_renders()[-1][1]
    if options.orbit_seconds > 0.0:
        for frame in orbit_frames(
            options.size, options.fps, options.orbit_seconds, labels, f"v030  {final_name}"
        ):
            writer.send(np.ascontiguousarray(frame))
            frames += 1

    writer.close()
    print(f"saved {options.output} ({frames} frames, {frames / options.fps:.1f} s)")


if __name__ == "__main__":
    main()
