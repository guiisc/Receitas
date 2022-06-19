import json
import streamlit as st
from scripts.db_manager import JsonManager

class InserReceita:
    def __init__(self) -> None:
        self.jmanager = JsonManager()
        self.front()
        return
    
    def to_json(self, nome, categorias, ingredientes, modoPreparo):
        """
        """
        json_f = {
            "Nome": nome,
            "Categorias": self.__strip_format(categorias.split(',')),
            "Ingredientes": self.__strip_format(ingredientes.split(',')),
            "ModoPreparo": self.__strip_format(modoPreparo.split(','))
        }
        return json_f
    
    def __strip_format(self, array):
        """
        """
        new_array = []
        for _ in array:
            new_array.append(_.strip())
        return new_array
    
    def front(self):
        st.markdown('# Nova Receita')
        st.write('Obs: ingredientes e categorias separados por vírgula, por favor')

        with st.form("Nova Receita", True):
            nome = st.text_input("Nome: ")
            categorias = st.text_input('Categorias: ')
            ingredientes = st.text_input('Ingredientes: ')
            st.text('Modo de Preparo:')
            
            modoPreparo = [st.text_input(f'{i+1}: ') for i in range(10)]
            
            submitted = st.form_submit_button("Inserir!")
            if submitted:
                new_receita = self.to_json(nome, categorias, ingredientes, modoPreparo)
                self.jmanager.salvar_receita(new_receita)
                st.write('Salvo!')
        return

ir = InserReceita()