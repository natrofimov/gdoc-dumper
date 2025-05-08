import re
from typing import AsyncGenerator, Generator

import httpx

from gdoc_dumper.enums import Formats
from gdoc_dumper.utils import logger


class Downloader:
    @staticmethod
    async def adownload(
        url: str,
        file_format: Formats = Formats.PDF,
        timeout: float = 10,
    ) -> bytes:
        """
        Asynchronously downloads a Google Docs document in the specified format.

        Args:
            url: Google Docs document url (Document must be public)
            file_format: The format to export the document to (default: PDF)
            timeout: Request timeout in seconds (default: 10)

        Returns:
            bytes: The content of the downloaded document

        Raises:
            ValueError: If the provided URL is not a valid Google Docs URL
            httpx.HTTPStatusError: If the HTTP request fails
        """

        id_match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", url)
        if id_match:
            doc_id = id_match.group(1)
        else:
            logger.error("Value Error: Invalid Google Docs url provided", exc_info=True)
            raise ValueError("Invalid Google Docs url provided")

        export_url = f"https://docs.google.com/document/d/{doc_id}/export?format={file_format.value}"

        async with httpx.AsyncClient() as client:
            logger.debug("Downloading gdoc: %s", export_url)
            response = await client.get(
                export_url,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()

            return response.content

    @staticmethod
    async def astream_download(
        url: str,
        file_format: Formats = Formats.PDF,
        chunk_size: int = 8192,
        timeout: float = 15,
    ) -> AsyncGenerator[bytes, None]:
        """
        Asynchronously downloads a Google Docs document in the specified format
        and returns the content as a stream of bytes.

        Args:
            url: Google Docs document url (Document must be public)
            file_format: The format to export the document to (default: PDF)
            chunk_size: Size of each chunk in bytes (default: 8192)
            timeout: Request timeout in seconds (default: 15)

        Yields:
            bytes: Chunks of the downloaded document

        Raises:
            ValueError: If the provided URL is not a valid Google Docs URL
            httpx.HTTPStatusError: If the HTTP request fails
        """
        id_match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", url)
        if id_match:
            doc_id = id_match.group(1)
        else:
            logger.error("Value Error: Invalid Google Docs url provided", exc_info=True)
            raise ValueError("Invalid Google Docs url provided")

        export_url = f"https://docs.google.com/document/d/{doc_id}/export?format={file_format.value}"

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "GET",
                export_url,
                timeout=timeout,
                follow_redirects=True,
            ) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                    yield chunk

    @staticmethod
    def download(
        url: str,
        file_format: Formats = Formats.PDF,
        timeout: float = 10,
    ) -> bytes:
        """
        Synchronously downloads a Google Docs document in the specified format.

        Args:
            url: Google Docs document url (Document must be public)
            file_format: The format to export the document to (default: PDF)
            timeout: Request timeout in seconds (default: 10)

        Returns:
            bytes: The content of the downloaded document

        Raises:
            ValueError: If the provided URL is not a valid Google Docs URL
            httpx.HTTPStatusError: If the HTTP request fails
        """

        id_match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", url)
        if id_match:
            doc_id = id_match.group(1)
        else:
            logger.error("Value Error: Invalid Google Docs url provided", exc_info=True)
            raise ValueError("Invalid Google Docs url provided")

        export_url = f"https://docs.google.com/document/d/{doc_id}/export?format={file_format.value}"

        with httpx.Client() as client:
            logger.debug("Downloading gdoc: %s", export_url)
            response = client.get(
                export_url,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()

            return response.content

    @staticmethod
    def stream_download(
        url: str,
        file_format: Formats = Formats.PDF,
        chunk_size: int = 8192,
        timeout: float = 15,
    ) -> Generator[bytes, None]:
        """
        Synchronously downloads a Google Docs document in the specified format
        and returns the content as a stream of bytes.

        Args:
            url: Google Docs document url (Document must be public)
            file_format: The format to export the document to (default: PDF)
            chunk_size: Size of each chunk in bytes (default: 8192)
            timeout: Request timeout in seconds (default: 15)

        Yields:
            bytes: Chunks of the downloaded document

        Raises:
            ValueError: If the provided URL is not a valid Google Docs URL
            httpx.HTTPStatusError: If the HTTP request fails
        """

        id_match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", url)
        if id_match:
            doc_id = id_match.group(1)
        else:
            raise ValueError("Invalid Google Docs url provided")

        export_url = f"https://docs.google.com/document/d/{doc_id}/export?format={file_format.value}"

        with httpx.Client() as client:
            with client.stream(
                "GET",
                export_url,
                timeout=timeout,
                follow_redirects=True,
            ) as response:
                response.raise_for_status()
                for chunk in response.iter_bytes(chunk_size=chunk_size):
                    yield chunk
