from django.test import TestCase
from django.contrib.auth.models import User
from compiler.models import Folder, File, Section

class FolderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.folder = Folder.objects.create(name='Test Folder', owner=self.user)

    def test_get_folders(self):
        subfolder = Folder.objects.create(name='Subfolder', parent=self.folder, owner=self.user)
        folders = self.folder.getFolders()
        self.assertEqual(folders.count(), 1)
        self.assertEqual(folders.first(), subfolder)

    def test_get_files(self):
        file = File.objects.create(name='Test File', folder=self.folder, owner=self.user)
        files = self.folder.getFiles()
        self.assertEqual(files.count(), 1)
        self.assertEqual(files.first(), file)

class FileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.folder = Folder.objects.create(name='Test Folder', owner=self.user)
        self.file = File.objects.create(name='Test File', folder=self.folder, owner=self.user)

    def test_file_has_folder(self):
        self.assertEqual(self.file.folder, self.folder)

class SectionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.folder = Folder.objects.create(name='Test Folder', owner=self.user)
        self.file = File.objects.create(name='Test File', folder=self.folder, owner=self.user)
        self.section = Section.objects.create(name='Test Section', file=self.file, owner=self.user)

    def test_section_has_file(self):
        self.assertEqual(self.section.file, self.file)
