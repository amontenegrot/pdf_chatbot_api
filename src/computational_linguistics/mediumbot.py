from .chatbot import ChatBot


class MediumBot(ChatBot):
    """
    A subclass of the ChatBot class that uses specific models for embeddings and GPT.

    This class inherits from the ChatBot class and overrides the `embedding_model` and `gpt_model` attributes 
    with specific models. The `embedding_model` is used for generating embeddings for chunks of text, 
    and the `gpt_model` is used for generating answers to questions based on a PDF document.
    """
    embedding_model = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'  # 1.11G
    gpt_model = 'gpt-3.5-turbo-0125'