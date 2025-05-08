from pathlib import Path
from typing import AsyncGenerator, Generator, Union

import aiofiles

from gdoc_dumper.utils import logger


class FileManager:
    @staticmethod
    async def asave_bytes(
        content: bytes,
        path: Union[str, Path],
    ) -> Path:
        path = Path(path)
        logger.debug("Saving file to: %s", path)
        async with aiofiles.open(path, "wb") as f:
            await f.write(content)

        return path

    @staticmethod
    async def asave_stream(
        stream: AsyncGenerator[bytes, None],
        path: Union[str, Path],
    ) -> Path:
        path = Path(path)
        logger.debug("Saving file to: %s", path)
        async with aiofiles.open(path, "wb") as f:
            async for chunk in stream:
                await f.write(chunk)

        return path

    @staticmethod
    def save_bytes(
        content: bytes,
        path: Union[str, Path],
    ) -> Path:
        path = Path(path)
        logger.debug("Saving file to: %s", path)
        with open(path, "wb") as f:
            f.write(content)

        return path

    @staticmethod
    def save_stream(
        stream: Generator[bytes, None],
        path: Union[str, Path],
    ) -> Path:
        path = Path(path)
        logger.debug("Saving file to: %s", path)
        with open(path, "wb") as f:
            for chunk in stream:
                f.write(chunk)

        return path
