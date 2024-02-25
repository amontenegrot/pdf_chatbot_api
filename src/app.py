import streamlit as st


st.header('ChatPDF')

chunk_size: int = st.slider(
    'Tamaño de las fracciones del texto',
    min_value=100, max_value=1000
    )
chunk_overlap: int = st.slider(
    'Tamaño de solapamientos entre fracciones de texto',
    min_value=10, max_value=100
    )

st.file_uploader(
    'Cargue su documento en formato pdf en la siguiente sección:',
    type='pdf'
    )

