import os

class createLogs():
    
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
        self.logs_filename = os.path.join(config.logs_path, config.logs_filename)
        if os.path.isfile(self.logs_filename):
            self.logs_file = open(self.logs_filename, 'a')
        else:
            self.logs_file = open(self.logs_filename, 'w')

    def write_log_csv(self, text_str):
        self.logs_file.write(text_str + '\n')

    def close_log_csv(self):
        self.logs_file.close()