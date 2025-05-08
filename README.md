# 📄 gdoc-dumper <br>
Lightweight python package for downloading Google Docs documents in various formats

# 🚀 Installation
Simply install with pip or another package manager:<br><br>
```pip install gdoc-dumper```

# 🔨 Usage<br>
## 🅰 Async
```python
import asyncio

from gdoc_dumper import Downloader, Formats, FileManager

# Asynchronously download google document as bytes
async def main() -> None:
    content: bytes = await Downloader.adownload(url="<GDOC URL>", file_format=Formats.PDF)
    # You also can save file after downloading it using FileManager
    await FileManager.asave_bytes(content, path="<DESIRED PATH as PATH or String>")

asyncio.run(main())
```
You also can stream download file and save it

```python
import asyncio
from typing import AsyncGenerator

from gdoc_dumper import Downloader, Formats, FileManager


async def main() -> None:
    stream: AsyncGenerator[bytes, None] = Downloader.astream_download(
        url="<GDOC URL>",
        file_format=Formats.PDF,
    )
    await FileManager.asave_stream(stream, path="file.pdf")


asyncio.run(main())
```

## 🔁 Sync
```python
from gdoc_dumper import Downloader, Formats, FileManager

# Download google document as bytes
content: bytes = Downloader.download(url="<GDOC URL>", file_format=Formats.PDF)

# You also can save file after downloading it using FileManager
path = FileManager.save_bytes(content, path="<DESIRED PATH as PATH or String>")

```

# ✅ Available formats
```python
from gdoc_dumper import Formats

print(Formats.TXT.value) # txt
print(Formats.PDF.value) # pdf
print(Formats.DOCX.value) # docx
print(Formats.EPUB.value) # epub
print(Formats.HTML.value) # html
print(Formats.OPEN_DOCUMENT_TEXT.value) # odt
print(Formats.RICH_TEXT.value) # rtf
print(Formats.ZIP.value) # zip
```

# ⭐ License
[MIT License]()