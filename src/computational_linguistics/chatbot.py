from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from typing import List, Any, Callable


class ChatBot:
    """
    A Superclass to represent a ChatBot that use a GPT model and a QA chain to answer questions based on a PDF document.
    """
    embedding_model = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'  # 471M
    gpt_model = 'gpt-3.5-turbo-0125'
    llm = ChatOpenAI(model_name=gpt_model)
    chain = load_qa_chain(llm, chain_type='stuff')

    def __init__(self, pdf_file_obj: Any, chunk_size: int, chunk_overlap: int, 
                 num_chunks_see: int, question: str) -> None:
        """
        Constructs all the necessary attributes for the ChatBot object.

        Args:
            pdf_file_obj (Any): The PDF file object to be processed.
            chunk_size (int): The size of the chunks to be created from the PDF text.
            chunk_overlap (int): The overlap size between consecutive chunks.
            num_chunks_see (int): The number of chunks to consider when generating embeddings.
            question (str): The question to be answered by the ChatBot.
        """
        self.pdf_file_obj = pdf_file_obj
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.num_chunks_see = num_chunks_see
        self.question = question

    def __pdf_text_extractor(self) -> str: #revisar el typing y la docstring
        """
        This method extracts the text from the PDF file associated with the ChatBot class object.
        Returns:
            str: A string containing all the text extracted from the PDF.
        """
        pdf_reader = PdfReader(self.pdf_file_obj)

        text = "".join(page.extract_text() for page in pdf_reader.pages)
        # del pdf_file_obj, pdf_reader  # Delete variables to free memory
        
        return text

    def __chunks_generator(self) -> List[str]:
        """
        This method generates chunks of text from a PDF.

        It uses the RecursiveCharacterTextSplitter to split the text extracted from the PDF into chunks. 
        The size and overlap of the chunks are determined by the chunk_size and chunk_overlap attributes of the class.

        Returns:
            List[str]: A list of string chunks from the PDF.
        """
        # Chunks creation
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
            )
        
        text = self.__pdf_text_extractor()
        chunks = text_splitter.split_text(text)
        
        return chunks

    def __embedding_generator(self) -> Any:
        """
        This method generates embeddings for chunks of text using HuggingFaceEmbeddings and FAISS.

        It uses the HuggingFaceEmbeddings to generate embeddings for the chunks of text. 
        The chunks are generated by the __chunks_generator method of the class.
        The embeddings are then used to create a knowledge base using FAISS.

        Returns:
            Any: A FAISS knowledge base created from the embeddings of the chunks of text.
        """
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        # model = SentenceTransformer(self.embedding_model)
        chunks: List[str] = self.__chunks_generator()

        knowledge_base: Any = FAISS.from_texts(chunks, embeddings)

        return knowledge_base
    
    def get_embeddings(self) -> List[Any]:
        """
        Generates embeddings for a given question using a knowledge base.

        This method first generates a knowledge base using the private method __embedding_generator.
        It then performs a similarity search on the knowledge base using the instance's question and num_chunks_see attributes.
        The method returns a list of documents (or chunks) that are most similar to the question.

        Returns:
            List[Any]: A list of documents that are most similar to the question.
        """
        knowledge_base = self.__embedding_generator()
        # Busqueda de párrafos similares
        docs = knowledge_base.similarity_search(self.question, self.num_chunks_see)

        return docs
    
    def system_qa(self) -> Any:
        """
        Generates an answer to a question using a knowledge base and a ChatGPT model.

        This method first retrieves embeddings for a given question using the get_embeddings method.
        It then uses these embeddings as input documents to provide context to a ChatGPT model.
        The method returns an answer generated by the ChatGPT model.

        Returns:
            Any: An answer generated by the ChatGPT model.
        """
        # Search for similar paragraphs
        docs = self.get_embeddings()

        # Use the similar paragraphs to provide context to ChatGPT
        answer = self.chain.run(input_documents=docs, question=self.question)
        
        return answer
    
    def calculate_cost(self) -> Callable:
        """
        Calculates the cost of generating an answer to a question using a knowledge base and a ChatGPT model.

        This method first retrieves embeddings for a given question using the get_embeddings method.
        It then uses these embeddings as input documents to provide context to a ChatGPT model.
        The method returns a callback function from the OpenAI API, which can be used to retrieve the cost of the operation.

        Returns:
            Callable: A callback function from the OpenAI API.
        """
        docs = self.get_embeddings()

        with get_openai_callback() as cb:
            response = self.chain.run(input_documents=docs, question=self.question)
            return cb
        