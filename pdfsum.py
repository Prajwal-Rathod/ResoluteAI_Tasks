import fitz  # PyMuPDF
import streamlit as st
from transformers import pipeline

def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Load summarization pipeline with a specified model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")

def summarize_text(text, max_length=500, min_length=30):
    max_chunk_length = 1024  # Adjust based on the model's maximum input length
    overlap = 100  # Define an overlap to maintain context between chunks

    # Split the text into overlapping chunks
    text_chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chunk_length, len(text))
        text_chunks.append(text[start:end])
        start = end - overlap  # Maintain overlap between chunks

    # Summarize each chunk and combine summaries
    summary = ""
    for chunk in text_chunks:
        summarized_chunk = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
        summary += summarized_chunk[0]['summary_text'] + " "

    # Ensure the final summary is close to 500 words
    summary_words = summary.split()
    if len(summary_words) > 500:
        summary = " ".join(summary_words[:500])

    return summary.strip()

# Function to load and display the PDF file
def load_pdf(pdf_file):
    return read_pdf(pdf_file)

# Streamlit app
st.title("PDF Summarizer")

pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_file is not None:
    # Read and display the content of the PDF
    pdf_text = load_pdf(pdf_file)
    st.write("Original Text:")
    st.text_area("Summary text", pdf_text, height=300)

    # Summarize the content
    summary = summarize_text(pdf_text)
    st.write("Summarized Text:")
    st.text_area("Summary", summary, height=300)
