import streamlit as st
from scripts import db_manager as db

class Front:
    def __init__(self):
        self.db = db.DBManager()
        self.nome_salvo = ''
        
        with st.container():
            st.title('Receitas')
        self.cont_consulta = st.container()
        self.cont_receita = st.container()
        return
    
    def run(self):
        self.__filter()
        self.receita()
        return
    
    def __filter(self):
        with self.cont_consulta:
            st.markdown('## Consulta')
            tabelas = {'Categorias': [], 'Ingredientes': []}
            col1, col2 = st.columns(2)
            
            with col1:
                c = 'Categorias'
                tabelas[c] = st.multiselect(
                        c,
                        self.db.check_columns(c))
            
            with col2:
                c = 'Ingredientes'
                tabelas[c] = st.multiselect(
                        c,
                        self.db.check_columns(c))
            self.__filter2(tabelas)
            return
        
    def __filter2(self, tabelas):
        """
        """
        with self.cont_consulta:
            table = self.db.filter(
                tabelas['Ingredientes'], tabelas['Categorias'])
            col1, col2, col3 = st.columns(3)
            col1.write('ID'); col2.write('Nome'); col3.write('Receita')
            for idx, row in table.iterrows():
                col1.write(row[1])
                col2.write(row[0])
                col3.button(f'{row[1]}', on_click=self.__button_filter, args=(row[1], row[0],))
        return
                
    def __button_filter(self, id, nome):
        """
        """
        with self.cont_receita:
            self.id_salvo = id
            self.nome_salvo = nome
            st.button(f'Gerar Receita {self.nome_salvo}', on_click=self.__passo_passo)
        return
    
    def receita(self):
        with self.cont_receita:
            st.markdown('---')
            st.markdown('## Receita')
        return
    
    def __passo_passo(self):
        """
        """
        with self.cont_receita:
            passo_passo = self.db.get_passo_passo(self.id_salvo).T
            passo_passo = passo_passo.iloc[1:]
            col1, col2 = st.columns(2)
            col1.write('Passo')
            col2.write('Receita')
            for idx, row in passo_passo.iterrows():
                col1.write(idx)
                col2.write(row[0])
            return

f = Front()
f.run()