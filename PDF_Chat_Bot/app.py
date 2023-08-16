import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

def get_pdf_text(pdf):
    """Extract text from a PDF document."""
    text = ''
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_text_chunks(raw_txt):
    """Extract chunks from raw text"""
    chunks = []

def main():
    load_dotenv()
    st.set_page_config(page_title = "Chat with PDF",page_icon=':books:')
    
    st.header('Chat with PDF :books:')
    st.text_input('Ask a question about your documents')

    with st.sidebar:
        st.subheader('Upload File Here!:open_file_folder:')
        pdf_doc = st.file_uploader('')
        if st.button('Process :heavy_check_mark:'):
            with st.spinner('Preprocessing'):
                #get text from pdf 
                raw_text = get_pdf_text(pdf_doc)
                      
            #convert into chunks
            text_chunks = get_text_chunks(raw_text)
            #create vector store   



if __name__ == '__main__':
    main()