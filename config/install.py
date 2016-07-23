import sys, os, logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#
# if 'install.py' in os.listdir('.'):  # the script is run from the config folder
#     append_path = '../'
# else:  # Class is called from the Root of the app
#     append_path = './'
# logger.info('append_path = %s', append_path)


sys.path.append('/Users/sladkovm/.virtualenvs/Users/sladkovm/Git/Velometria_streams')
logger.info('PYTHONPATH = %s', '\n'.join(sys.path))