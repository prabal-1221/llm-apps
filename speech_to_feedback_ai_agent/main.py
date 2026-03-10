import asyncio

from graph import build_graph
from utils import setup_logger

# Initialize Logger
setup_logger()

async def main():
    feedback_generator = build_graph()

    inputs = {
        "questions": [],
        "idx": 0,
    }

    await feedback_generator.ainvoke(inputs)

if __name__ == "__main__":
    asyncio.run(main())
