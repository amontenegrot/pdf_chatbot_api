from .chatbot import ChatBot


class LargeBot(ChatBot):
    embedding_model = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'  # 1.11G
    gpt_model = 'gpt-3.5-turbo-instruct'