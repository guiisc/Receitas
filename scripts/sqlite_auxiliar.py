import sqlite3
from . import pd

class SQLCommands:
    def __init__(self):
        """
        """
        self.IDs = {
            'Receitas': 'id_receitas',
            'Categorias': 'id_categorias',
            'Ingredientes': 'id_ingredientes',
            'ModoPreparo': 'id_modopreparo',
            'Calendario': 'dia'}
        self.f = lambda x: x.replace('[', '(').replace(']', ')').replace("', '", "','")
        return
    
    def init_db(self, name):
        """
        Return connector for name DataBase
        """
        conn = sqlite3.connect(name)
        return conn
    
    def create_table_receitas(self, conn):
        """
        """
        statment = """
            CREATE TABLE IF NOT EXISTS Receitas(
                id_receitas INTEGER PRIMARY KEY,
                nome CHAR(50) NOT NULL
            )
        """
        conn.execute(statment)
        return
    
    def create_table_categorias(self, conn):
        """
        """
        statment = """
            CREATE TABLE IF NOT EXISTS Categorias(
                id_categorias INTEGER PRIMARY KEY,
                FOREIGN KEY (id_categorias) REFERENCES Receitas(id_receitas)
            )
        """
        conn.execute(statment)
        return
    
    def create_table_ingredientes(self, conn):
        """
        """
        statment = """
            CREATE TABLE IF NOT EXISTS Ingredientes(
                id_ingredientes INTEGER PRIMARY KEY,
                FOREIGN KEY (id_ingredientes) REFERENCES Receitas(id_receitas)
            )
        """
        conn.execute(statment)
        return
    
    def create_table_modopreparo(self, conn):
        """
        """
        passos = str([f'passo_{i} CHAR(200)' for i in range(10)]).replace("'", '')[1:-1]
        
        statment = f"""
            CREATE TABLE IF NOT EXISTS ModoPreparo(
                id_modopreparo INTEGER PRIMARY KEY,
                {passos},
                FOREIGN KEY (id_modopreparo) REFERENCES Receitas(id_receitas)
            )
        """
        conn.execute(statment)
        return
    
    def create_table_calendario(self, conn):
        statment = f"""
            CREATE TABLE IF NOT EXISTS Calendario(
                dia CHAR(10),
                Almoco CHAR(100),
                Lanche CHAR(100),
                Janta CHAR(100),
                Sobremesa CHAR(100)
            )
        """
        conn.execute(statment)
        return
        
    def delete_row_calendar(self, conn, date):
        statment = f"""
            DELETE FROM Calendario
            WHERE dia = {date};
        """
        conn.execute(statment)
        return
    
    def insert_row(self, conn, table, values):
        """
        values (list)
        """
        columns = f'{self.check_columns(conn, table)}'
        values = f'{values}'
        
        statment = f"""
            INSERT INTO {table}{self.f(columns)}
            VALUES{self.f(values)}
        """
        cursor = conn.cursor()
        cursor.execute(statment)
        conn.commit()
        return
    
    def insert_columns(self, conn, table, values):
        """
        """
        for value in values:
            statment = f"""
                ALTER TABLE {table}
                ADD '{value}' BOLL DEFAULT(FALSE);
            """
            cursor = conn.cursor()
            cursor.execute(statment)
            conn.commit()
        return
    
    def check_tables(self, conn):
        """
        Return all tables name in the DataBase's connector
        """
        query = """
        SELECT name FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
        """
        table = conn.execute(query)
        return table.fetchall()
    
    def check_columns(self, conn, table):
        """
        Return all column names in table
        """
        query = f"""
        PRAGMA table_info({table})
        """
        table = conn.execute(query).fetchall()
        return [i[1] for i in table]
    
    def check_last_id(self, conn, table):
        _id = self.IDs[table]
        query = f"""
            SELECT {_id} FROM {table}
            ORDER BY {_id} DESC
            LIMIT 1;
        """
        table = conn.execute(query).fetchall()
        if len(table) < 1:
            return -1
        return table[0][0]
    
    def consult_ingredientes(self, ingredientes):
        flag_ingre = True
        if len(ingredientes) > 0:
            query_ingre = f"WHERE ingredientes.{ingredientes[0]} = TRUE"
            for _ in ingredientes:
                query_ingre += f""" AND ingredientes.{_} = TRUE
                """
        else:
            query_ingre = ""
            flag_ingre = False
        return query_ingre, flag_ingre
    
    def consult_categorias(self, categorias, ingre=False):
        if len(categorias) > 0:
            if ingre:
                query_cate = ""
            else:
                query_cate = f"""WHERE categorias.{categorias[0]} = TRUE
                """
            
            for _ in categorias:
                query_cate += f"""AND categorias.{_} = TRUE
                """
        else:
            query_cate = ""
        return query_cate
        
    def consult_(self, conn, ingredientes = [], categorias = []):
        query_base = f"""
            SELECT receitas.nome, receitas.id_receitas FROM receitas
            JOIN categorias ON categorias.id_categorias=receitas.id_receitas
            JOIN ingredientes ON ingredientes.id_ingredientes=receitas.id_receitas
            """
        
        query_cate = ""
        
        query_ingre, flag_ingre = self.consult_ingredientes(ingredientes)
        query_cate = self.consult_categorias(categorias, flag_ingre)
        
        table = conn.execute(
            query_base + query_cate + query_ingre + ";").fetchall()
        return table
        
    def get_passo_passo(self, conn, id_receitas):
        """
        """
        query = f"""
            SELECT * from ModoPreparo
            WHERE id_modopreparo = {id_receitas};
        """
        table = conn.execute(
            query).fetchall()
        return table
        
    def get_refeicao(self, conn, date):
        """
        """
        query = f"""
            SELECT * FROM Calendario
            ;
        """
        table = conn.execute(
            query).fetchall()
        return table