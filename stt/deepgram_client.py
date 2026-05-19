import os
import asyncio

from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    LiveOptions,
    LiveTranscriptionEvents
)

# -----------------------------------
# LOAD ENV
# -----------------------------------

load_dotenv()

DEEPGRAM_API_KEY = os.getenv(
    "DEEPGRAM_API_KEY"
)

# -----------------------------------
# MAIN CLASS
# -----------------------------------

class DeepgramStreamingClient:

    def __init__(self):

        self.transcript_queue = (
            asyncio.Queue()
        )

        self.last_transcript = ""

        self.dg_connection = None

    # -----------------------------------
    # CONNECT
    # -----------------------------------

    async def connect(self):

        try:

            deepgram = DeepgramClient(
                DEEPGRAM_API_KEY
            )

            # ✅ FINAL FIX FOR SDK v7
            self.dg_connection = (
                deepgram.listen.asynclive.v("1")
            )

            # -----------------------------------
            # TRANSCRIPT CALLBACK
            # -----------------------------------

            async def on_message(
                self_client,
                result,
                **kwargs
            ):

                sentence = (
                    result.channel
                    .alternatives[0]
                    .transcript
                )

                if not sentence:
                    return

                if result.is_final:

                    if (
                        sentence
                        ==
                        self.last_transcript
                    ):

                        print(
                            "DUPLICATE IGNORED"
                        )

                        return

                    self.last_transcript = (
                        sentence
                    )

                    confidence = (
                        result.channel
                        .alternatives[0]
                        .confidence
                    )

                    print(
                        "FINAL:",
                        sentence
                    )

                    print(
                        "CONF:",
                        confidence
                    )

                    await (
                        self.transcript_queue
                        .put({
                            "text": sentence,
                            "confidence": confidence,
                            "is_final": True
                        })
                    )

            # -----------------------------------
            # REGISTER EVENTS
            # -----------------------------------

            self.dg_connection.on(
                LiveTranscriptionEvents.Transcript,
                on_message
            )

            # -----------------------------------
            # OPTIONS
            # -----------------------------------

            options = LiveOptions(

                model="nova-2",

                language="en-US",

                encoding="linear16",

                channels=1,

                sample_rate=16000,

                interim_results=True,

                punctuate=True
            )

            # -----------------------------------
            # START CONNECTION
            # -----------------------------------

            await self.dg_connection.start(
                options
            )

            print(
                "✅ Deepgram connected"
            )

        except Exception as e:

            print(
                "❌ DEEPGRAM ERROR:",
                str(e)
            )

    # -----------------------------------
    # SEND AUDIO
    # -----------------------------------

    async def send_audio(
        self,
        audio_chunk
    ):

        try:

            if self.dg_connection:

                await (
                    self.dg_connection
                    .send(audio_chunk)
                )

        except Exception as e:

            print(
                "❌ AUDIO SEND ERROR:",
                str(e)
            )

    # -----------------------------------
    # GET TRANSCRIPT
    # -----------------------------------

    async def get_transcript(self):

        return await (
            self.transcript_queue.get()
        )