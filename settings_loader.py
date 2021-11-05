from configparser import ConfigParser

def config_loader(path):
    config = ConfigParser()
    config.read(path)
    return config

def camera_settings(path):
    settings = {}
    cfg = 'camera'
    config=config_loader(path)
    settings['framerate'] = int(config.get(cfg,'framerate'))
    settings['resolution'] = list(map(int, config.get(cfg, 'resolution').split(', ')))
    settings['shutter_speed'] = int(config.get(cfg, 'shutter_speed'))
    settings['awb_mode'] = str(config.get(cfg, 'awb_mode'))
    settings['exposure_mode'] = str(config.get(cfg, 'exposure_mode'))
    settings['sensor_mode'] = int(config.get(cfg, 'sensor_mode'))
    settings['iso'] = int(config.get(cfg, 'iso'))
    settings['awb_gains'] = tuple(map(int, config.get(cfg, 'auto_white_balance_gains').split(', ')))
    settings['horizontal_flip'] = eval(str(config.get(cfg, 'horizontal_flip')))
    settings['vertical_flip']= eval(str(config.get(cfg, 'vertical_flip')))
    settings['Display'] = eval(str(config.get(cfg,'Display')))
    return settings


def pi_settings(path):
    settings = {}
    cfg =  'pi'
    config=config_loader(path)
    settings['user_interrupt_only'] = eval(str(config.get(cfg, 'user_interrupt_only')))
    settings['data_path']= config.get(cfg, 'data_root')
    settings['duration'] = int(config.get(cfg, 'duration'))
    settings['rfid'] = eval(str(config.get(cfg, 'rfid')))
    settings['nreaders'] = int(config.get(cfg, 'nreaders'))
    settings['spt'] = eval(str(config.get(cfg,'spt')))
    settings['port'] = int(config.get(cfg,'spt'))
    settings['ip'] = config.get(cfg, 'ip')
    return settings