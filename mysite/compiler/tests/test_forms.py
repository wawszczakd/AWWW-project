from django.test import TestCase
from compiler.forms import *

class FolderFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'parent': None,
            'name': 'Test Folder',
            'description': 'Folder description',
        }
        form = FolderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'name': '',
            'description': 'Folder description',
        }
        form = FolderForm(data=form_data)
        self.assertFalse(form.is_valid())

class DeleteFolderFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'parent': None,
        }
        form = DeleteFolderForm(data=form_data)
        self.assertTrue(form.is_valid())

class FileFormTest(TestCase):
    def test_invalid_form(self):
        form_data = {
            'upload': None,
            'name': '',
            'description': 'File description',
        }
        form = FileForm(data=form_data)
        self.assertFalse(form.is_valid())

class DeleteFileFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'file': None,
        }
        form = DeleteFileForm(data=form_data)
        self.assertTrue(form.is_valid())
