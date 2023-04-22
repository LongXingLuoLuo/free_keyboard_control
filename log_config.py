import logging
import os.path
import logging.config
configPath = r'./log.conf'
configFile = open(configPath, 'r', encoding='UTF-8')
logging.config.fileConfig(configFile)
logger = logging.getLogger(name='fileLogger')
configFile.close()
