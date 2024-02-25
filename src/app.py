import os

import streamlit as st

from computational_linguistics import SmallBot


st.header('ChatPDF')

chunk_size: int = st.slider(
    'Tamaño de las fracciones del texto:',
    min_value=100, max_value=1000, value=500
    )
chunk_overlap: int = st.slider(
    'Tamaño de solapamientos entre fracciones de texto:',
    min_value=10, max_value=100, value=30
    )

num_chunks_see = st.slider('Número de fracciones a contemplar:',
    min_value=1, max_value=10, value=2
    )

OPENAI_API_KEY = st.text_input(
    'Ingrese la API key configurada en su cuenta de OpenAI.',
    type='password'
    )

pdf_file_obj = st.file_uploader(
    'Cargue su documento en formato pdf en esta sección:',
    type='pdf'
    )

if pdf_file_obj:
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    question = st.text_input('Realice su pregunta:')
    chat_pdf = SmallBot(
        pdf_file_obj=pdf_file_obj,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        num_chunks_see=num_chunks_see,
        question=question
    )

    answer = chat_pdf.system_qa()
    cost = chat_pdf.calculate_cost()

    st.write(answer)
    st.write(cost)
