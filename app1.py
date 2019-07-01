# coding:utf-8
"""
runs the App class
the run consists of
    1) set language
    2) print a translatable message
    
the translations are prepared with pygettext/poedit
and stored as domain 'app' in the appropriate directories/files underneath locale directory
following languages exists
    en is the default language (no translation exists)
    de has a translation
    fr has a translation
"""
import os
import sys
import gettext

class App():
    
    def set_language(self, language):
        """
        configures the requested translation (parameter language) and
        sets the global function alias _() to either
            the requested translation or to
            the default language in case of error of in case of default language is requested
        """

        global _                                    # ensures _ in builtin namespace is treated by lang.install()

        try:
            lang = gettext.translation("app",localedir='locale', languages=[language])
            lang.install()                          # installs gettext function _() to language 'language'
        except FileNotFoundError as fnfe:
            sys.stderr.write(str(fnfe) + "\n")
            gettext.install("app")                  # resets gettext function _() to default language
    
    def print_test(self):
        """
        prints an arbitrary message in requested language
        """
        
        print(_("environment variable '{}' not set").format('LANGUAGE'))
        
    def run(self, language):

        self.set_language(language)
        self.print_test()

if __name__ == '__main__':
    app = App()
    language=''
    app.run(language)