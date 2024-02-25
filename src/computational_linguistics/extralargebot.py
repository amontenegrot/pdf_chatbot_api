from .chatbot import ChatBot


class ExtraLargeBot(ChatBot):
    embedding_model = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'  # 1.11G
    gpt_model = 'gpt-4-32k'