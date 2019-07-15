# coding:utf-8
"""
Shows how to use class-based gettext.
(same features as app1, but different configuration)

Creates an instance of the class App 
and executes its run method using several languages/translations.

Eeach run consists of

1. language initialization, 
2. translations initialization, 
3. print of a test message.

For orientation purposes, the application **logs**

- each language change
- each translation initialization failure (in real live, only a fallback to default language should happen)

In preparation, the translations has been building with pygettext/poedit.

The **built translation files** reside in the appropriate structure where

:<language>: is the code of the appropriate language and 
:<domain>: is always 'app'

::

    locale/<language>/LC_MESSAGES/<domain>.mo (compiled translation)
    locale/<language>/LC_MESSAGES/<domain>.po (translation in plain text)

So, appropriate gettext parameters are 

:domain: 'app'
:localedir: 'locale'
:languages: [<language>] 

For **testing purposes** the script is using the following languages/translations

:en: is the default language (no translation exists)
:de: has a translation
:fr: has a translation
:es: no translation exists (triggers fallback to default language)

So, **expected result** for each language is 

:en: test message in default language English, error message due to missing (English) translation
:de: test message in German language
:fr: test message in French language
:es: test message in default language English, error message due to missing (Spanish) translation

These cases can be also checked by running the **unit-test script** tests/test_app2_01.py.

(until here same features as app1, furthermore:)

Configuration by class Config (and so via cfg-file app.cfg)

"""
import sys
import gettext
from config import Config


class App():
    
    def __init__(self):
        """
        setup configuration via class Config and cfg-file
        init the language
        """
        self._config = Config('app')
        self._cfg = self._config.get_config_parser()
        
        self._language = None
        self.set_language()

    def set_language(self, language = Config.LANGUAGE_DEFAULT):
        """
        set language as requested resp. to the default language if no language parameter is passed
        """
        self._language = language
        print('language set to {}'.format(self._language))

    def get_language(self):
        return self._language
    
    def set_translation(self, language = Config.LANGUAGE_DEFAULT):
        """
        configure the translation
        set the global function alias _() to either
        
        - the requested language or to
        - the default language in case of error of in case of default language is requested
        
        """

        global _                                    # ensures _ in builtin namespace is treated by lang.install()

        localedir = self._cfg[Config.PATHS][Config.DIR_LOCALE]

        try:
            lang = gettext.translation(self._config.get_app(),localedir=localedir, languages=[language])
            lang.install()                          # installs gettext function _() to language 'language'
        except FileNotFoundError as fnfe:
            sys.stderr.write(str(fnfe) + "\n")
            gettext.install(self._config.get_app()) # resets gettext function _() to default language
    
    def test_print(self):
        """
        print message in configured/currently chosen translation
        """
        
        print(_("This is a test message. Translated from default language 'en' to '{}'").format(self.get_language()))
        
    def run(self, language = Config.LANGUAGE_DEFAULT):

        self.set_language(language)
        self.set_translation(language)
        self.test_print()

if __name__ == '__main__':
    app = App()
    app.run()
    app.run('de')
    app.run('fr')
    app.run('es')