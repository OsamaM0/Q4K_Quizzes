import json
import os
import hashlib
import asyncio
import re
from aiofiles import open as aio_open  # Use aiofiles for asynchronous file handling
from bot.modules.re_link import RE_LINK

class QuizDataHandler:
    _lock = asyncio.Lock()  # Class-level lock for shared access control across instances

    def __init__(self, json_file="quiz_data.json"):
        self.json_file = json_file
        self.data = {}
        self.data_loaded = asyncio.Event()  # Event to signal when data is fully loaded
        asyncio.create_task(self._load_data())

    async def _load_data(self):
        """Load data from the JSON file asynchronously if it exists."""
        if os.path.exists(self.json_file):
            async with QuizDataHandler._lock:  # Ensure shared lock
                async with aio_open(self.json_file, 'r', encoding='utf-8') as f:
                    file_content = await f.read()
                    self.data = json.loads(file_content)
        else:
            self.data = {"youtube": {}, "documents": {}}

        self.data_loaded.set()  # Signal that the data has been loaded

    async def _save_data(self):
        """Save current data back to the JSON file asynchronously with shared lock."""
        await self.data_loaded.wait()  # Ensure data is loaded before saving
        async with QuizDataHandler._lock:  # Ensure shared lock
            async with aio_open(self.json_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(self.data, ensure_ascii=False, indent=4))
                
    @staticmethod
    async def hash_content(content):
        """Generate an MD5 hash for the given content."""
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    async def add_entry(self, source, text_or_content, chunks=None, summarization=None):
        """
        Automatically add a YouTube or document entry based on the source type.
        """
        await self.data_loaded.wait()  # Ensure data is loaded before adding an entry

        if chunks is None:
            chunks = {}

        domain = await RE_LINK.get_domain(source) if source else None
        if domain in ["youtube.com", "youtu.be"]:
            await self.set_youtube_entry(source, text_or_content, chunks, summarization)
        else:
            await self.set_document_entry(source, text_or_content, chunks, summarization)

    async def set_entry(self, identifier, text_or_content, chunks=None, summarization=None, entry_type="youtube"):
        """
        General function to set data for both YouTube and documents, appending chunks if they exist.
        """
        await self.data_loaded.wait()  # Ensure data is loaded before setting an entry

        if chunks is None:
            chunks = {}

        # Retrieve existing entry or create a new one
        if entry_type == "youtube":
            entry = self.data["youtube"].get(identifier, {"text": text_or_content, "questions": {}, "summarization": None})
        elif entry_type == "documents":
            identifier  = await self.hash_content(text_or_content)
            entry = self.data["documents"].get(identifier, {"text": text_or_content, "questions": {}, "summarization": None})
        else:
            return

        # Update the text and summarization if provided
        entry["text"] = text_or_content
        entry["summarization"] = summarization

        # Append new questions to the existing chunks
        for chunk_key, new_chunk in chunks.items():
            if chunk_key not in entry["questions"]:
                entry["questions"][chunk_key] = []
            existing_chunk = entry["questions"][chunk_key]
            for question in new_chunk:
                if not any(q['question'] == question['question'] for q in existing_chunk):
                    existing_chunk.append(question)

        # Save the updated entry
        if entry_type == "youtube":
            self.data["youtube"][identifier] = entry
        elif entry_type == "documents":
            self.data["documents"][identifier] = entry

        await self._save_data()

    async def get_entry(self, identifier, content, entry_type=None):
        """
        Retrieve either a YouTube entry (if identifier is a valid YouTube URL) 
        or a document entry (if identifier is document content).

        :param identifier: The YouTube link or document content hash.
        :param content: Document content for documents or URL for YouTube.
        :param entry_type: Force the type ("youtube" or "documents"), optional. If not provided, it is inferred.
        :return: Dictionary containing text, questions, and summarization or None if not found.
        """
        await self.data_loaded.wait()  # Ensure data is loaded before retrieving an entry

        YOUTUBE_URL_REGEX = re.compile(r'(https?://)?(www\.)?(youtube|youtu)(\.com|\.be)/[a-zA-Z0-9\-_]{11}')

        # Check if the identifier_or_content is a valid YouTube link
        if entry_type == "youtube" or (entry_type is None and bool(YOUTUBE_URL_REGEX.match(identifier))):
            # If it's a YouTube link, retrieve the YouTube entry
            return self.data["youtube"].get(identifier, {"text": None, "questions": {}, "summarization": None})

        # Otherwise, treat it as document content and get the hash
        else:
            # Hash the document content
            doc_hash = await self.hash_content(content)
            # Check for document entry using the hash
            return self.data["documents"].get(doc_hash, {"text": None, "questions": {}, "summarization": None})

        # Return None if no valid entry is found
        return None

    async def get_questions(self, identifier, content, entry_type=None):
        """
        Retrieve the questions for a YouTube entry or document entry.
        """
        return (await self.get_entry(identifier, content, entry_type)).get("questions", {})

    async def get_summarization(self, identifier, content, entry_type=None):
        """
        Retrieve the summarization for a YouTube entry or document entry.
        """
        return (await self.get_entry(identifier, content, entry_type)).get("summarization", None)

    async def get_text(self, identifier_or_content, entry_type=None):
        """
        Retrieve the text for a YouTube entry or document entry.
        """
        return (await self.get_entry(identifier_or_content, identifier_or_content, entry_type)).get("text", None)

    ##############################################################################################
    ################################# YOUTUBE Entry Methods ######################################
    ##############################################################################################

    async def set_youtube_entry(self, youtube_link, text, chunks=None, summarization=None):
        """Set or update the text, chunked questions, and summarization for a given YouTube link."""
        await self.set_entry(youtube_link, text, chunks, summarization, entry_type="youtube")

    async def get_youtube_entry(self, youtube_link):
        """Retrieve the text, questions (by chunks), and summarization for a given YouTube link."""
        return await self.get_entry(youtube_link, youtube_link, entry_type="youtube")

    async def remove_youtube_entry(self, youtube_link):
        """Remove the YouTube entry for a given YouTube link."""
        await self.data_loaded.wait()  # Ensure data is loaded before removing an entry
        if youtube_link in self.data["youtube"]:
            del self.data["youtube"][youtube_link]
            await self._save_data()

    ##############################################################################################
    ################################ Document Entry Methods ######################################
    ##############################################################################################
    async def set_document_entry(self, youtube_link, text, chunks=None, summarization=None):
        """Set or update the text, chunked questions, and summarization for a given YouTube link."""
        await self.set_entry(youtube_link, text, chunks, summarization, entry_type="documents")
        
    async def set_document_chunk(self, document_content, text_range, new_questions):
        """Update questions for a specific text range chunk of a given document."""
        await self.data_loaded.wait()  # Ensure data is loaded before setting chunks

        doc_hash = await self.hash_content(document_content)
        document_data = await self.get_entry(doc_hash, document_content, entry_type="documents")

        existing_chunks = document_data['questions']
        if text_range not in existing_chunks:
            existing_chunks[text_range] = []

        existing_questions = existing_chunks[text_range]
        for new_question in new_questions:
            if not any(q['question'] == new_question['question'] for q in existing_questions):
                existing_questions.append(new_question)

        await self.set_entry(doc_hash, document_content, existing_chunks, document_data['summarization'], entry_type="documents")

    async def remove_document_entry(self, document_content):
        """Remove the document entry based on its content."""
        await self.data_loaded.wait()  # Ensure data is loaded before removing an entry

        doc_hash = await self.hash_content(document_content)
        if doc_hash in self.data["documents"]:
            del self.data["documents"][doc_hash]
            await self._save_data()
