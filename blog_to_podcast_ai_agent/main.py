import asyncio

from graph import build_graph
from utils import setup_logger

# Initialize Logger
setup_logger()

async def main():
    podcast_generator = build_graph()

    inputs = {
        "url": "https://blog.google/innovation-and-ai/technology/safety-security/the-quantum-era-is-coming-are-we-ready-to-secure-it/",
        "content": None,
        "flg_content": False,
        "script": None,
        "flg_script": False
    }

    await podcast_generator.ainvoke(inputs)

if __name__ == "__main__":
    asyncio.run(main())
