from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback


class ChatBot:
    """
    Define una clase Chatbot
    """
    gpt_model = 'gpt-3.5-turbo-0125'  # gpt-3.5-turbo  #revisar si es posible eliminarla
    llm = ChatOpenAI(model_name=gpt_model)
    chain = load_qa_chain(llm, chain_type='stuff')

    def __init__(self, pdf_path: str, chunk_size: int, chunk_overlap: int, 
                 num_chunks_see: int, question: str):
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.num_chunks_see = num_chunks_see
        self.question = question

    def __pdf_text_extractor(self)->str: #revisar el typing y la docstring
        # Read pdf
        pdf_file_obj = open(self.pdf_path, 'rb')
        pdf_reader = PdfReader(pdf_file_obj)

        text = "".join(page.extract_text() for page in pdf_reader.pages)

        pdf_file_obj.close()  # Free up system resources
        del pdf_file_obj, pdf_reader  # Delete variables to free memory
        
        return text

    def __chunks_generator(self):
        # Chunks creation
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
            )
        
        text = self.__pdf_text_extractor()
        chunks = text_splitter.split_text(text)
        
        return chunks

    def __embedding_generator(self):
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        model = SentenceTransformer(self.embedding_model)  #revisar si esta linea hace algo o solo es usada para probar los embedings
        chunks = self.__chunks_generator()

        knowledge_base = FAISS.from_texts(chunks, embeddings)

        return knowledge_base
    
    def get_embeddings(self) -> str: #revisar el typing y la docstring
        knowledge_base = self.__embedding_generator()
        # Busqueda de párrafos similares
        docs = knowledge_base.similarity_search(self.question, self.num_chunks_see)

        return docs
    
    def system_qa(self):
        # Busqueda de párrafos similares
        docs = self.get_embeddings(self.question, self.num_chunks_see)

        # Utilizar los parrafos similares para darle contexto a ChatGPT
        answer = self.chain.run(input_documents=docs, question=self.question)
        
        return answer
        # print(f'Respuesta ChatGPT:\n\t {answer}')
    
    def calculate_cost(self):
        docs = self.get_embeddings(self.question, self.num_chunks_see)

        with get_openai_callback() as cb:
            response = self.chain.run(input_documents=docs, question=self.question)
            return cb
        
class SmallBot(ChatBot):
    embedding_model = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'  # 471M
    gpt_model = 'gpt-3.5-turbo-0125'

class MediumBot:
    embedding_model = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'  # 1.11G
    gpt_model = 'gpt-3.5-turbo-0125'

class LargeBot:
    embedding_model = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'  # 1.11G
    gpt_model = 'gpt-3.5-turbo-instruct'

class ExtraLargeBot:
    embedding_model = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'  # 1.11G
    gpt_model = 'gpt-4-32k'