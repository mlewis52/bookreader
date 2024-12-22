import os
from openai import OpenAI
from pathlib import Path
import pymupdf # This is PyMuPDF
import time 

class PDFReader:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file using PyMuPDF"""
        try:
            # Open the PDF
            doc = fitz.open(pdf_path)
            
            # Extract text from all pages
            text = ""
            for page in doc:
                text += page.get_text() + "\n"
                
            doc.close()
            return text
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
            return None

    def split_text_into_chunks(self, text, max_chars=4000):
        """Split text into smaller chunks, trying to break at sentences"""
        # Split into sentences (roughly)
        sentences = text.replace('\n', ' ').split('.')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip() + '.'  # Add the period back
            if current_length + len(sentence) + 1 <= max_chars:
                current_chunk.append(sentence)
                current_length += len(sentence) + 1
            else:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = len(sentence)
                
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks

    def text_to_speech(self, text, output_filename, voice="alloy"):
        """Convert text to speech using OpenAI's API"""
        try:
            speech_file_path = Path(output_filename)
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            response.stream_to_file(speech_file_path)
            return True
        except Exception as e:
            print(f"Error in text to speech conversion: {str(e)}")
            return False

    def process_pdf(self, pdf_path, voice="alloy"):
        """Process entire PDF and convert to speech"""
        # Extract text from PDF
        print("Reading PDF...")
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return False

        # Split into chunks
        print("Processing text...")
        chunks = self.split_text_into_chunks(text)
        
        # Create output directory if it doesn't exist
        output_dir = Path("audio_output")
        output_dir.mkdir(exist_ok=True)
        
        # Process each chunk
        print(f"Converting to speech... ({len(chunks)} chunks)")
        for i, chunk in enumerate(chunks):
            output_file = output_dir / f"part_{i+1}.mp3"
            print(f"Converting chunk {i+1} of {len(chunks)}...")
            success = self.text_to_speech(chunk, output_file, voice)
            if not success:
                print(f"Failed to convert chunk {i+1}")
            time.sleep(1)  # Small delay to avoid rate limiting
            
        print(f"Conversion complete! Audio files saved in {output_dir}")
        return True

def main():
    # Get PDF path from user
    pdf_path = input("Enter the path to your PDF file: ")
    
    # Get voice preference
    print("\nAvailable voices:")
    print("1. alloy - Neutral and balanced")
    print("2. echo - Mature and deep")
    print("3. fable - Warm and friendly")
    print("4. onyx - Professional and authoritative")
    print("5. nova - Bright and energetic")
    print("6. shimmer - Clear and youthful")
    
    voice_choice = input("\nChoose a voice (1-6) [default: alloy]: ").strip()
    voice_options = {
        "1": "alloy",
        "2": "echo",
        "3": "fable",
        "4": "onyx",
        "5": "nova",
        "6": "shimmer"
    }
    voice = voice_options.get(voice_choice, "alloy")
    
    # Create reader and process PDF
    reader = PDFReader()
    reader.process_pdf(pdf_path, voice)

if __name__ == "__main__":
    main()