from transformers import pipeline

# Load a pre-trained summarization model
summarizer = pipeline("summarization", model="t5-small")

def summarize_abstract(abstract_text):
    # Summarize the abstract
    summary = summarizer(abstract_text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Example abstract
abstract = """
The study investigates the role of dust in regulating star formation rates in galaxies. Using observations from 
the Hubble Space Telescope and simulations, we quantify the relationship between dust content and stellar 
population growth. The findings suggest that dust plays a crucial role in shielding molecular gas from UV 
radiation, thereby promoting star formation in certain galactic environments.
"""

# Generate summary
summary = summarize_abstract(abstract)
print("Summary:", summary)

# Add an Interface with Streamlit

import streamlit as st

# Title of the app
st.title("Research Abstract Summarizer")

# Text input for the abstract
abstract_input = st.text_area("Enter Research Abstract", height=200)

if st.button("Summarize"):
    if abstract_input.strip():
        with st.spinner("Generating summary..."):
            summary = summarize_abstract(abstract_input)
            st.subheader("Summary")
            st.write(summary)
    else:
        st.warning("Please enter an abstract.")

# Add Extraction Capability

from PyPDF2 import PdfFileReader

def extract_abstract_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PdfFileReader(file)
        num_pages = reader.getNumPages()
        
        # Look through all pages for the abstract section
        for page_num in range(num_pages):
            page = reader.getPage(page_num)
            text = page.extract_text()
            if "Abstract" in text:
                return text.split("Abstract")[1].split("\n")[0]
    return "Abstract not found."

# Integrate into the Interface
# Allow users to upload a PDF and extract abstracts for summarization.

uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type="pdf")

if uploaded_file is not None:
    with st.spinner("Extracting abstract..."):
        abstract_text = extract_abstract_from_pdf(uploaded_file)
        st.subheader("Extracted Abstract")
        st.write(abstract_text)
        if st.button("Summarize Abstract"):
            summary = summarize_abstract(abstract_text)
            st.subheader("Summary")
            st.write(summary)
