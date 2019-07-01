# coding:utf-8
'''
tests for the module app1
'''
import unittest
import os
import sys
from contextlib import contextmanager
from io import StringIO
import app2

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
        self.app = app2.App()
        app2_path = os.path.dirname(app2.__file__)
        os.chdir(app2_path)

    def tearDown(self):
        self.app = None

    def test_language_empty(self):
        
        with self.captured_output() as (out, err):
            self.app.set_language("")
            self.app.print_test()
        out_msg = out.getvalue().strip()
        err_msg = err.getvalue().strip()
        self.assertEqual(err_msg, "")
        self.assertEqual(out_msg, "environment variable 'LANGUAGE' not set", "empty language error")

    def test_language_default(self):
        
        with self.captured_output() as (out, err):
            self.app.set_language("en")
            self.app.print_test()
        out_msg = out.getvalue().strip()
        err_msg = err.getvalue().strip()
        self.assertEqual(err_msg, "")
        self.assertEqual(out_msg, "environment variable 'LANGUAGE' not set", "default language error")


    def test_language_known_de(self):
 
        with self.captured_output() as (out, err):
            self.app.set_language("de")
            self.app.print_test()
        out_msg = out.getvalue().strip()
        err_msg = err.getvalue().strip()
        self.assertEqual(err_msg, "", "error")
        self.assertEqual(out_msg, "Umgebungsvariable 'LANGUAGE' nicht festgelegt", "known language 'de' error")

    def test_language_known_fr(self):
 
        with self.captured_output() as (out, err):
            self.app.set_language("fr")
            self.app.print_test()
        out_msg = out.getvalue().strip()
        err_msg = err.getvalue().strip()
        self.assertEqual(err_msg, "", "error")
        self.assertEqual(out_msg, "variable de l'environnement 'LANGUAGE' ne pas definé", "known language 'fr' error")

    def test_language_unknown_es(self):

        with self.captured_output() as (out, err):
            self.app.set_language("es")
            self.app.print_test()
        out_msg = out.getvalue().strip()
        err_msg = err.getvalue().strip()
        self.assertEqual(err_msg, "[Errno 2] No translation file found for domain: 'app'", "unknown language 'es' error")
        self.assertEqual(out_msg, "environment variable 'LANGUAGE' not set", "unknown language 'es' error")
