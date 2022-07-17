import streamlit as st
import scripts.db_manager as dbm_class
DB = dbm_class.DBManager()

class CalendarioClass():
    def __init__(self) -> None:
        self.__base()
        pass
    
    def __base(self):
        with st.container():
            st.write("# Calendário")
            self.date = st.date_input("Dia", on_change=self.__changes)
            st.markdown('---')
        return
    
    def __changes(self):
        date = self.date
        with st.container():
            st.write("## Output")
            self.calendario_hoje = DB.get_calendario(str(date))
            st.dataframe(
                DB.to_pd("Calendario", self.calendario_hoje).sort_values('Dia'))

            st.write("## Input")
            if len(self.calendario_hoje[0]) < 1:
                default = [""]*4
            else:
                default = list(self.calendario_hoje[0])[1:]
            with st.form("form_calendario", True):
                almoco = st.text_input("Almoço: ", value=default[0])
                lanche = st.text_input("Lanche: ", value=default[1])
                janta = st.text_input("Jantar: ", value=default[2])
                sobremesa = st.text_input("Sobremesas: ", value=default[3])
                
                submitted = st.form_submit_button("Submit!")
                if submitted:
                    values = [
                        str(date),
                        almoco, lanche, janta, sobremesa
                        ]
                    DB.add_calendar(values)
                    st.write('Salvo!')
            return

c = CalendarioClass()