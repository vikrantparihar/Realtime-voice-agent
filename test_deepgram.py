import asyncio

from stt.deepgram_client import (
    DeepgramStreamingClient
)


async def main():

    client = (
        DeepgramStreamingClient()
    )

    await client.connect()

    print(
        "Deepgram connected successfully"
    )

    while True:

        transcript = (
            await client.get_transcript()
        )

        print(
            "FINAL:",
            transcript
        )


asyncio.run(main())