import streamlit as st
import os

st.write(f"""
        # BEM VINDO
        <div style="text-align: right;">by: Guilherme Silva</div>
        
        ---
        
        Este site é pra ser colaborativo (provavelmente não)
        para ajudar a decidir o que comer e trocar receitas

""", unsafe_allow_html=True)

if 'Receitas.db' in os.listdir('data/'):
        with open('data/Receitas.db', 'rb') as f:
                st.download_button(
                        label="Download Database",
                        data=f,
                        file_name='Receitas.db',
                        mime='application/octet-stream'
                )