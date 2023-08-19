import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

#for creating chunks
from langchain.text_splitter import CharacterTextSplitter

#for word embedding
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS

#for buffer memory and conversation chain
from langchain.memory import ConversationBufferMemory

from langchain.chains import ConversationalRetrievalChain

from langchain.chat_models import ChatOpenAI
from template import css,user_template,bot_template

from langchain.llms import HuggingFaceHub

def get_pdf_text(pdf):
    """Extract text from a PDF document."""
    text = ''
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_text_chunks(raw_txt):
    """Extract chunks from raw text"""
    text_spliter = CharacterTextSplitter(
        separator='\n',
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len        
    )
    chunks = text_spliter.split_text(raw_txt)
    return chunks

#use this function for faster processing and is a paid version
def get_vector_store_openAPI(chunks):
    """
        Exttract and maintain word embedding from chunks of text 

    """
    embeddings = OpenAIEmbeddings()
    vector_stores = FAISS.from_texts(chunks,embedding=embeddings)
    
    return vector_stores

def get_vector_store(chunks):
    """
        Exttract and maintain word embedding from chunks of text 

    """
    embeddings = HuggingFaceInstructEmbeddings(model_name ='hkunlp/instructor-base' )
    vector_stores = FAISS.from_texts(texts=chunks,embedding=embeddings)
    
    return vector_stores


def get_conversation_chain(vector_store):
    #for faster communication uncomment the following line and comment line after that
    #llm = ChatOpenAI()
    llm = HuggingFaceHub(repo_id='google/flan-t5-xxl',
                         model_kwargs = {'temperature':0.5,
                                         'max_length':512})

    
    memory = ConversationBufferMemory(memory_key='chat_history',return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory = memory
    )
    return conversation_chain
   
def handle_user_input(question):
    response = st.session_state.conversation({'question':question})
    st.session_state.chat_history = response['chat_history']
    
    for i,message in enumerate(st.session_state.chat_history):
        #for odd side i.e user side msg
        if i%2 == 0:
            st.write(user_template.replace('{{MSG}}',message.content),unsafe_allow_html=True)
        else: #for bot side conversation
            st.write(bot_template.replace('{{MSG}}',message.content),unsafe_allow_html=True)
        
        
def main():
    load_dotenv()
    st.set_page_config(page_title = "Chat with PDF",page_icon=':books:')
    
    st.write(css,unsafe_allow_html=True)
    
    if 'conversation' not in st.session_state:
        st.session_state.conversation = None
        
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None
        
    st.header('Chat with PDF :books:')
    user_question = st.text_input('Ask a question about your documents')
    
    if user_question:
        handle_user_input(user_question)
    
        
    with st.sidebar:
        st.subheader('Upload File Here!:open_file_folder:')
        pdf_doc = st.file_uploader('Upload the file or Drag and drop below. Then click on proceed!')
       
        if st.button('Process :heavy_check_mark:'):
            with st.spinner('Preprocessing'):
                #get text from pdf 
                raw_text = get_pdf_text(pdf_doc)
                    
                #convert into chunks
                text_chunks = get_text_chunks(raw_text)
            
            
                #create vector store 
                vectors_store = get_vector_store(text_chunks)
            

                #create conversation chain
                st.session_state.conversation = get_conversation_chain(vectors_store)
           
            


if __name__ == '__main__':
    main()