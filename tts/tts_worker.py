import asyncio

from tts.elevenlabs_client import (
    generate_speech
)


# -----------------------------------
# NORMAL TTS
# -----------------------------------

async def generate_audio_async(
    text
):

    audio = await asyncio.to_thread(
        generate_speech,
        text
    )

    return audio


# -----------------------------------
# STREAMING TTS
# -----------------------------------

async def stream_tts_audio(
    text,
    chunk_size=4096
):

    # -----------------------------------
    # GENERATE FULL AUDIO
    # -----------------------------------

    audio_bytes = await (
        generate_audio_async(
            text
        )
    )

    # -----------------------------------
    # SAFETY
    # -----------------------------------

    if not audio_bytes:

        return

    # -----------------------------------
    # STREAM IN CHUNKS
    # -----------------------------------

    for i in range(

        0,
        len(audio_bytes),
        chunk_size

    ):

        chunk = audio_bytes[
            i:i + chunk_size
        ]

        yield chunk

        # -----------------------------------
        # SMALL STREAM DELAY
        # -----------------------------------

        await asyncio.sleep(
            0.02
        )