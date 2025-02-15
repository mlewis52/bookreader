PDF to Speech Converter
A Python application that converts PDF documents to audio using OpenAI's Text-to-Speech API. This tool automatically splits large documents into manageable chunks and converts them to high-quality audio files using various AI voices.
Features

PDF text extraction using PyMuPDF
Smart text chunking to handle large documents
Multiple AI voice options
Automatic audio file generation
Progress tracking during conversion
Rate limiting protection

Prerequisites

Python 3.x
OpenAI API key
Required Python packages:

openai
PyMuPDF (imported as fitz)
pathlib
python-dotenv (recommended for API key management)
