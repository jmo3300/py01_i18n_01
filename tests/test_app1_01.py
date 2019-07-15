# coding:utf-8
'''
tests for the module app1
'''
import unittest
import os
import sys
from contextlib import contextmanager
from io import StringIO
import app1 as app

class Test(unittest.TestCase):

    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def setUp(self):
        self.app = app.App()
        app_path = os.path.dirname(app.__file__)
        os.chdir(app_path)

    def tearDown(self):
        self.app = None


    def test_language_default(self):

        self.app.set_language()
        with self.captured_output() as (out, err):
            self.app.set_translation()
            self.app.test_print()
        out_msg = out.getvalue().strip()
        err_msg = err.getvalue().strip()
#         print(out_msg)
#         print(err_msg)
        self.assertEqual(err_msg, "[Errno 2] No translation file found for domain: 'app'", "unknown default language error")
        self.assertEqual(out_msg, "This is a test message. Translated from default language 'en' to 'en'")

    def test_language_known_de(self):

        language = "de" 
        self.app.set_language(language)
        with self.captured_output() as (out, err):
            self.app.set_translation(language)
            self.app.test_print()
        out_msg = out.getvalue().strip()
        err_msg = err.getvalue().strip()
#         print(out_msg)
#         print(err_msg)
        self.assertEqual(err_msg, "", "error")
        self.assertEqual(out_msg, "Dieses ist eine Test-Meldung. Übersetzt aus der Vorgabe-Sprache 'en' nach 'de'")

    def test_language_known_fr(self):
 
        language = "fr" 
        self.app.set_language(language)
        with self.captured_output() as (out, err):
            self.app.set_translation(language)
            self.app.test_print()
        out_msg = out.getvalue().strip()
        err_msg = err.getvalue().strip()
#         print(out_msg)
#         print(err_msg)
        self.assertEqual(err_msg, "", "error")
        self.assertEqual(out_msg, "C'est une message de test. Traduit de la langue par défault 'en' en fr'")

    def test_language_unknown_es(self):

        language = "es" 
        self.app.set_language(language)
        with self.captured_output() as (out, err):
            self.app.set_translation(language)
            self.app.test_print()
        out_msg = out.getvalue().strip()
        err_msg = err.getvalue().strip()
#         print(out_msg)
#         print(err_msg)
        self.assertEqual(err_msg, "[Errno 2] No translation file found for domain: 'app'", "unknown language 'es' error")
        self.assertEqual(out_msg, "This is a test message. Translated from default language 'en' to 'es'")
