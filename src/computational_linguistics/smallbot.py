from chatbot import ChatBot


class SmallBot(ChatBot):
    embedding_model = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'  # 471M
    gpt_model = 'gpt-3.5-turbo-0125'