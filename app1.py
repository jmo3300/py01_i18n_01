# coding:utf-8
"""
Shows how to use class-based gettext.

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

These cases can be also checked by running the **unit-test script** tests/test_app1_01.py.

"""
import os
import sys
import gettext

class App():
    """
    Application for showing how to use class-based gettext
    
    Usage:
    ::

        app = App()   
        app.run()        # run with default language
        app.run('de')    # run with german language
    
    
    """
    
    LANGUAGE_DEFAULT = 'en'
    
    def __init__(self):
        """
        init the language
        """
        self._language = None
        self.set_language()

    def set_language(self, language = LANGUAGE_DEFAULT):
        """
        set language as requested resp. to the default language if no language parameter is passed
        """
        self._language = language
        print('language set to {}'.format(self._language))

    def get_language(self):
        return self._language
    
    def set_translation(self, language = LANGUAGE_DEFAULT):
        """
        configure the translation
        set the global function alias _() to either
        
        - the requested language or to
        - the default language in case of error of in case of default language is requested
        
        """

        global _                                    # ensures _ in builtin namespace is treated by lang.install()

        try:
            lang = gettext.translation("app",localedir='locale', languages=[language])
            lang.install()                          # installs gettext function _() to language 'language'
        except FileNotFoundError as fnfe:
            sys.stderr.write(str(fnfe) + "\n")
            gettext.install("app")                  # resets gettext function _() to default language
    
    def test_print(self):
        """
        print message in configured/currently chosen translation
        """
        
        print(_("This is a test message. Translated from default language 'en' to '{}'").format(self.get_language()))
        
    def run(self, language = LANGUAGE_DEFAULT):
        """
        run prepare and conduct a test
        
        - set language
        - set translation
        - print a test message
        
        """
        self.set_language(language)
        self.set_translation(language)
        self.test_print()

if __name__ == '__main__':
    print(os.path.abspath('.'))
    print(os.path.abspath('..'))
    app = App()
    app.run()
    app.run('de')
    app.run('fr')
    app.run('es')