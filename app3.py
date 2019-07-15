# coding:utf-8
"""
Simultaneous implementation of class-based and non-class-based gettext

Problem: implementation with class-based gettext, argparse with non-class-based gettext
---------------------------------------------------------------------------------------
In course of an implementation the class-based gettext has been applied. 
Then, argparse has been added to the implementation. 
As i18n solution for argparse only non-class-based gettext solutions has been finding.
For guarding the former implementation a solution for using simultaneously both approaches has been searching.

Solution: simultaneous usage / appliance of class-based and non-class-based gettext
-----------------------------------------------------------------------------------

class-based gettext uses an instance of *Translation class
non-class-based gettext uses an environment variable (LC_MESSAGES is used in this app)

In case of argparse usage/help-output:

::

    Starten mit:app3.py [-h] [-o] [-t] [-v] filename
    
    Positionsargumente:
      filename
    
    optionale Argumente:
      -h, --help       zeige diese Hilfe-Nachricht an und beende das Programm
      -o, --overwrite  vorhandene "Stichproben"-Tabelle überschreiben
      -t, --templates  Erzeuge Vorlagen-Dateien
      -v, --verbose    Erhöhe Detaillierung der Programm-Meldungen

All translations come from domain 'argparse' (file locale/de/LC_MESSAGES/argparse.mo) 
except the help messages of the optional arguments which come from domain 'app' (file locale/de/LC_MESSAGES/app.mo)

So, for getting a homogeneous translation output both solutions have to be serving separately.
In the run function all variances are tried

- homogeneous output in default language
- homogeneous output in foreign language
- mixed output in default and in foreign language

Run this application with -h option
-----------------------------------

It's the best way to see the mixture of argparse-based and application-based translations.


i18n - apply class-based gettext
================================

Create and run the App class
the run consists of

1) init language
2) init translations
3) print tests while changing languages and translations
    
In preparation, the translations has been building with pygettext/poedit.

The built translation files reside in the appropriate structure where

:<language>: is the code of the appropriate language and 
:<domain>: is always 'app'

::

    locale/<language>/LC_MESSAGES/<domain>.mo (compiled translation)
    locale/<language>/LC_MESSAGES/<domain>.po (translation in plain text)

So, appropriate gettext parameters are 

:domain: 'app'
:localedir: 'locale'
:languages: [<language>] 

For testing purposes the script is using the following languages/translations

:en: is the default language (no translation exists)
:de: has a translation
:fr: has a translation
:es: no translation exists (triggers fallback to default language)

(until here same features as app1, furthermore:)

Configuration by class Config (and so via cfg-file app.cfg)

(until here same features as app2, furthermore:)

i18n for argparse
=================
non-class-based solution as described in 
post 5 of https://stackoverflow.com/questions/22951442/how-to-make-pythons-argparse-generate-non-english-text
works properly for argparse but not for the individual help messages of the added arguments.

In the following solution 

    the translation of the internal argparse messages 

        is done by using a seperate domain (here 'argparse') via none-class-based gettext and

    the translation of the individual argparse help messages

        is done by using the application domain (here 'app') via class-based gettext

"""
import os
import sys
import gettext
import argparse
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
        print("language set to '{}'".format(self._language))

    def get_language(self):
        return self._language
    
    def set_LC_MESSAGES(self, language = Config.LANGUAGE_DEFAULT):
        os.environ['LC_MESSAGES'] = language
        print("environment variable 'LC_MESSAGES' set to '{}'".format(language))
    
    def set_translation(self, language = Config.LANGUAGE_DEFAULT):
        """
        configure the translation
        set the global function alias _() to either
            the requested language or to
            the default language in case of error of in case of default language is requested
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
        
    def test_parse(self):

        
        parser = argparse.ArgumentParser()
        parser.add_argument('filename')
        parser.add_argument('-o', '--overwrite', help=_('overwrite existing "samples" worksheet'), action='store_true')
        parser.add_argument('-t', '--templates', help=_('create templates files'), action='store_true')
        parser.add_argument('-v', '--verbose', help=_('increase output verbosity'), action='store_true')
        try:
            parser.parse_args()
        except:
            pass        
        
    def run(self):

        # gettext configuration by non-class way for internationalization of argparse
        localedir = self._cfg[Config.PATHS][Config.DIR_LOCALE]        
        gettext.bindtextdomain('argparse', localedir)
        gettext.textdomain('argparse')

        self.set_language()
        self.set_translation()
        self.test_print()
        self.set_language("fr")
        self.set_translation("fr")
        self.test_print()
        self.set_language("de")
        self.set_translation("de")
        self.test_print()

        print('\n')
        self.set_LC_MESSAGES('de')
        self.set_language("de")
        self.set_translation('de')
        print('\n')
        print("proper (homogeneous) output in foreign language")
        print("-----------------------------------------------")
        self.test_parse()

        print('\n')
        self.set_LC_MESSAGES()
        self.set_language()
        self.set_translation()
        print('\n')
        print("proper (homogeneous) output in default language")
        print("-----------------------------------------------")
        self.test_parse()

        print('\n')
        self.set_LC_MESSAGES()
        self.set_language('de')
        self.set_translation('de')
        print('\n')
        print("inproper (mixed) output in default language and in foreign language")
        print("-------------------------------------------------------------------")
        self.test_parse()
                
        print('\n')
        self.set_language()
        self.set_translation()
        self.test_print()
        self.set_language("fr")
        self.set_translation("fr")
        self.test_print()
        self.set_language("de")
        self.set_translation("de")
        self.test_print()

if __name__ == '__main__':
    app = App()
    app.run()
