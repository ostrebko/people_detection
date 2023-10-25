from utils.camera_acc import getCameraAcc
from utils.read_config import config_reader


if __name__ == '__main__':
    
    config = config_reader('config/data_config.json')
    getCameraAcc(config).get_camera_acc()