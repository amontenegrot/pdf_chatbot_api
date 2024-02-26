# ChatPDF
This project performs Natural Language Processing (NLP) tasks as a question/answer system for a PDF file by implementing the Object Oriented Programming paradigm, Embedding and the OpenAi API.

It uses the Streamlit library for the user interface, LangChain for language processing, and the OpenAI API to interact with ChatGPT.

# Installation

To install the necessary dependencies for this project, you can use pip:

```bash
pip install -r requirements.txt
```

# Usage
To start the Streamlit application, run the following command in your terminal:

```bash
streamlit run app.py
```
# Code Structure
The code is organized using Object-Oriented Programming (OOP) principles. Here is an overview of the main classes:

* ChatBot: A Superclass to represent a ChatBot that use a GPT model and a QA chain to answer questions based on a PDF document.
* SmallBot: A subclass of the ChatBot class that uses specific models for embeddings and GPT.
* MediumBot: A subclass of the ChatBot class that uses specific models for embeddings and GPT.
* LargeBot: A subclass of the ChatBot class that uses specific models for embeddings and GPT.
* ExtraLargeBot: A subclass of the ChatBot class that uses specific models for embeddings and GPT.

## UML diagram

```mermaid
classDiagram
    class ChatBot {
        -embedding_model: string
        -gpt_model: string
        -llm: Any
        -chain: Any
        +pdf_file_obj: Any
        +chunk_size: int
        +chunk_overlap: int
        +num_chunks_see: int
        +question: string
        -pdf_text_extractor(): string
        -chunks_generator(): List
        -embedding_generator(): Any
        +get_embeddings(): List
        +system_qa(): Any
        +calculate_cost(): Callable
    }

    class SmallBot {
        -embedding_model: string
        -gpt_model: string
    }

    class MediumBot {
        -embedding_model: string
        -gpt_model: string
    }

    class LargeBot {
        -embedding_model: string
        -gpt_model: string
    }

    class ExtraLargeBot {
        -embedding_model: string
        -gpt_model: string
    }

    ChatBot <|-- SmallBot
    ChatBot <|-- MediumBot
    ChatBot <|-- LargeBot
    ChatBot <|-- ExtraLargeBot
```

# Contribution
Contributions to this project are welcome. Please open an issue to discuss your ideas before making a pull request.

# License
This project is licensed under the MIT license.