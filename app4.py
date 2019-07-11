# coding:utf-8
"""
configures the requested translation (parameter language) and
sets the global function alias _() to either
    the requested translation or to
    the default language in case of error of in case of default language is requested
(same features as app1,) furthermore
uses config as used in real application
"""
import sys
import gettext
from config import Config

class App():
    
    def __init__(self):
        self._config = Config('app')
        self._cfg = self._config.get_config_parser()
        self.set_translation()
  
    def set_translation(self, language="en"):
        """
        configures the requested translation (parameter language) and
        sets the global function alias _() to either
            the requested translation or to
            the default language in case of error or in case of default language is requested
        """
        global _                                    # ensures _ in builtin namespace is treated by lang.install()
        
        if language == "" or language == Config.LANGUAGE_DEFAULT :
            gettext.install(self._config.get_app()) # resets gettext function _() to default language
            return 

        localedir = self._cfg[Config.PATHS][Config.DIR_LOCALE]
        
        try:
            lang = gettext.translation(self._config.get_app(), localedir=localedir, languages=[language])
            lang.install()                          # installs gettext function _() to language 'language'
        except FileNotFoundError as fnfe:
            sys.stderr.write(str(fnfe) + "\n")
            gettext.install(self._config.get_app()) # resets gettext function _() to default language
    
    def print_test(self):
        
        print(_("environment variable '{}' not set").format('LANGUAGE'))
        
    def run(self):
        
        self.print_test()
        self.set_translation("de")
        self.print_test()
        self.set_translation("fr")
        self.print_test()


if __name__ == '__main__':
    app = App()
    app.run()