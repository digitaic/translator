import asyncio
import edge_tts

TEXT = "Hiii,  I'm Joooeee.  Where did you arrive?  Want to drink something?"
VOICE = "en-GB-SoniaNeural"
OUTPUT_FILE = "test2.mp3"


async def amain() -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE)
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                print(f"WordBoundary: {chunk}")

if __name__== "__main__":
    asyncio.run(amain())





