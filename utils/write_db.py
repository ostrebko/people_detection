import os
import sqlite3

class createLogsDB():
    
    """
    Class descriptions ...
    
    Params:
    ----------
    ....
    
    name: descr ....
    
    """ 
    
    
    def __init__(self, config: dict):
        self.config = config
        if not os.path.exists(config.logs_path):
            os.makedirs(config.logs_path)
        self.logs_filename = os.path.join(config.logs_path, config.db_filename)
        
        self.connection = sqlite3.connect(self.logs_filename)
        self.cursor = self.connection.cursor()

        # Создаем таблицу Detections
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Detections (
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        num_people INTEGER
        )
        ''')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON Detections (time)')

    
    def add_db(self, date, time, num_people):
        self.cursor.execute('INSERT INTO Detections (date, time, num_people) VALUES (?, ?, ?)', 
               (date, time, num_people))
        self.connection.commit()
        
    def close_db(self):
        self.connection.close()