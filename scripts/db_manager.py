from . import json, np, pd, json, os
from . import sqlite_auxiliar

class DBManager:
    def __init__(self):
        self.sql = sqlite_auxiliar.SQLCommands()
        
        self.path = 'data/'
        self.temp_file_name = 'temp_add.json'
        self.db_name = 'Receitas.db'
        
        self.__init_db()
        return
    
    def __init_db(self):
        self.conn = self.sql.init_db(f'{self.path}{self.db_name}')
        self.__create_tables()
        return
    
    def __create_tables(self):
        """
        """
        self.sql.create_table_receitas(self.conn)
        self.sql.create_table_categorias(self.conn)
        self.sql.create_table_ingredientes(self.conn)
        self.sql.create_table_modopreparo(self.conn)
        self.sql.create_table_calendario(self.conn)
        return
    
    def to_pd(self, table_name, table):
        """
        """
        columns = self.check_columns(table_name)
        columns.insert(0, "Dia")
        df = pd.DataFrame(table, columns=columns)
        return df
        
    
    def check_tables(self):
        """
        """
        tables = self.sql.check_tables(self.conn)
        tables = [str(i)[2:-3] for i in tables]
        return tables
    
    def check_columns(self, table):
        """
        """
        columns = self.sql.check_columns(self.conn, table)
        return columns[1:]
    
    def check_last_id(self, table):
        """
        """
        return self.sql.check_last_id(self.conn, table)
    
    def read_new(self):
        """
        """
        with open(f'{self.path}{self.temp_file_name}') as f:
            file = json.load(f)
        return file
    
    def add(self):
        """
        """
        file = self.read_new()
        for table in file:
            values = np.array(file[table])
            
            if table == 'Nome':
                values = [file[table]]
                table = 'Receitas'
            elif table == 'ModoPreparo':
                values = np.append(values, ['-']*(10-len(values)))
            else:
                values = np.array(list(map(lambda x: x.replace(' ', '_'), values)))
                existed_columns = self.sql.check_columns(self.conn, table)
                new_columns = map(
                                lambda x: x.replace(' ', '_'),
                                values[np.isin(values, existed_columns) == False])
                new_columns = list(new_columns)
                self.sql.insert_columns(self.conn, table, new_columns)
                
                existed_columns = np.array(self.sql.check_columns(self.conn, table))
                
                values = np.isin(existed_columns, values)[1:]
            
                
            self.__add(table, list(values))
        return
            
    
    def __add(self, table, values):
        values.insert(
            0,
            self.sql.check_last_id(self.conn, table) + 1)
        return self.sql.insert_row(self.conn, table, values)
    
    def add_calendar(self, values):
        self.sql.delete_row_calendar(self.conn, values[0])
        self.sql.insert_row(self.conn, "Calendario", values)
        return
    
    def filter(self, ingredientes, categorias):
        table =  self.sql.consult_(self.conn, ingredientes, categorias)
        return pd.DataFrame(table, columns=['Nome', 'id'])
    
    def get_passo_passo(self, id):
        table = self.sql.get_passo_passo(self.conn, id)
        return pd.DataFrame(table)
    
    def get_calendario(self, date):
        table = self.sql.get_refeicao(self.conn, date)
        return table

class JsonManager:
    def __init__(self) -> None:
        self.path='data/'
        self.file_name = 'all.json'
        self.temp_file_name = 'temp_add.json'
        pass
    
    def create_json(self, temp=False):
        """
        """
        if temp:
            name = self.temp_file_name
        else:
            name = self.file_name
        
        if not self.file_name in os.listdir(self.path):
            with open(f'{self.path}{name}', 'w') as f:
                json.dump({}, f)
        return
            
    def delete_temp(self):
        """
        """
        os.remove(f'{self.path}{self.temp_file_name}')
        return
    
    def read_json(self):
        self.create_json()
        with open(f'{self.path}{self.file_name}', 'r') as f:
            file = json.load(f)
        return file
    
    def save_json(self, file, temp=False):
        if temp:
            name = self.temp_file_name
        else:
            name = self.file_name
        
        with open(f'{self.path}{name}', 'w') as f:
            json.dump(file, f)
        return True
    
    def salvar_receita(self, new_receita):
        file = self.read_json()
        file[f"{len(file)+1}"] = new_receita
        self.save_json(file)
        return True
    
    def reindex(self, file):
        """
        """
        new_file = {}
        for num, item in enumerate(file):
            new_file[f"{num}"] = item
        return new_file
        