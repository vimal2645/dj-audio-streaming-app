from __future__ import annotations

import io

from .remix import remix_audio


def run_remix_job(
    audio_bytes: bytes,
    track_2_bytes: bytes | None,
    options: dict,
):
    """Run one isolated render without importing the Streamlit UI."""
    audio_file = io.BytesIO(audio_bytes)
    track_2_file = io.BytesIO(track_2_bytes) if track_2_bytes else None
    return remix_audio(audio_file, track_2_file=track_2_file, **options)