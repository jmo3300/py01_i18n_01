# coding:utf-8

import os
from os.path import abspath, dirname, join
import logging
from configparser import ConfigParser

class Constants:
    """
    Extract of all constants used within configuration context. Class Config should be the only subclass.
    Constants are used in form "Config.<CONSTANT_NAME>"
    The separation of constants and code increases/should increase the handling during development.
    """
    
    GENERAL = 'general'

    LANGUAGE = 'language'
    
    LOCALE = 'locale'
    LC_MESSAGES = 'LC_MESSAGES'
    
    LANGUAGE_EN = 'en'
    LANGUAGE_DE = 'de'
    LANGUAGE_FR = 'fr'
    LANGUAGE_DEFAULT = LANGUAGE_EN
    LANGUAGES = [
        LANGUAGE_DEFAULT,
        LANGUAGE_DE,
        LANGUAGE_FR,
        ]
    
    PATHS = 'paths'
    
    DIR_LOCALE = 'dir.locale'
    DIR_LOCALE_DEFAULTNAME = 'locale'
    DIR_LOGS = 'dir.logs'
    DIR_LOGS_DEFAULTNAME = 'logs'

class Config(Constants):
    """
    Inititializes / Provides appropriate access methods to 
    
    - cfg file
    - paths
    - log
    
    """

    cfg = ConfigParser()

    def __init__(self, app):
        
        self._app = app

        self._cfg_filename = join(dirname(abspath(__file__)), self.get_app() + ".cfg")

        try:
            with open(self._cfg_filename):
                self.cfg.read(self._cfg_filename)
        except IOError:
            self._create_config()

        self.check_paths()

        self._init_log()
    
    def _create_config(self):

        root_directory = dirname(abspath(__file__))
        locale_directory = os.path.join(root_directory, Config.DIR_LOCALE_DEFAULTNAME)
        logs_directory = os.path.join(root_directory, Config.DIR_LOGS_DEFAULTNAME)

        self.cfg[Config.GENERAL] = {
            Config.LANGUAGE: Config.LANGUAGE_DEFAULT,
            }

        self.cfg[Config.PATHS] = {
            Config.DIR_LOCALE: locale_directory,
            Config.DIR_LOGS: logs_directory,
            }
        
        with open(self.get_config_filename(), 'w') as config_file:
            self.cfg.write(config_file)
        
    def _init_log(self):
        
        # TODO: separate log file per run
        # LOG
        self._log = logging.getLogger(self.get_app())
        self._log.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(logging.DEBUG)
        self._log.addHandler(sh)
        
        file_name = os.path.join(self.cfg[Config.PATHS][Config.DIR_LOGS], self.get_app() + '.log')
        fh = logging.FileHandler(file_name, mode='a')
        fh.setFormatter(fmt)
        fh.setLevel(logging.DEBUG)
        self._log.addHandler(fh)

    def get_app(self):
        return self._app
    
    def get_log(self):
        return self._log
    
    def get_config_filename(self):
        return self._cfg_filename
    
    def get_config_parser(self):
        return self.cfg

    def check_paths(self):
        self.check_path(self.cfg[Config.PATHS][Config.DIR_LOGS])

    def check_path(self, directory):
        path = join(dirname(abspath(__file__)), directory)
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
