import streamlit as st
import scripts.db_manager as dbm_class


class Insert:
    def __init__(self) -> None:
        self.jm = dbm_class.JsonManager()
        self.dbm = dbm_class.DBManager()
        
        self.cont_all = st.container()
        self.cont_detail = st.container()
        self.__front()
        self.__detail()
        return
    
    def __front(self):
        with self.cont_all:
            st.markdown('# Inserção')
            self.__show_pendencies()
        return
        
    def __show_pendencies(self):
        with self.cont_all:
            self.file = self.jm.read_json()
            col1, col2 = st.columns(2)
            
            for idx in self.file:
                with col1:
                    st.write(self.file[idx]['Nome'])
                
                with col2:
                    st.button('Show', key=idx, on_click=self.__show_pendency, args=(idx, ))
        return
    
    def __detail(self):
        with self.cont_detail:
            st.markdown('# Detail')
        return
    
    def __show_pendency(self, idx):
        with self.cont_detail:
            st.json(self.file[f"{idx}"])
            col1, col2 = st.columns(2)
            
            with col1:
                st.button('Aprovar', on_click=self.__aprovado, args=(idx,))
            
            with col2:
                st.button('Apagar', on_click=self.__reprovado, args=(idx,))
        return
    
    def __aprovado(self, idx):
        self.jm.create_json(temp=True)
        self.jm.save_json(self.file[f'{idx}'], temp=True)
        self.dbm.add()
        self.jm.delete_temp()
        self.__reprovado(idx)
        return
    
    def __reprovado(self, idx):
        del self.file[f'{idx}']
        self.file = self.jm.reindex(self.file)
        self.jm.save_json(self.file)
        return
i = Insert()