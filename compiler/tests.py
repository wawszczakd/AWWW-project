from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from compiler.models import *
from compiler.forms import *
from django.core.files.uploadedfile import SimpleUploadedFile

file_content = b'Test file content'
file_name = 'test_file.txt'

file_upload = SimpleUploadedFile(file_name, file_content)

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

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.folder = Folder.objects.create(name='Test Folder', owner=self.user)
        self.file = File.objects.create(name='Test File', owner=self.user)
    
    def test_start_view(self):
        response = self.client.get(reverse('compiler:start'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/start.html')
    
    def test_register_view_get(self):
        response = self.client.get(reverse('compiler:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/register.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)
        self.assertContains(response, 'Register')
    
    def test_register_view_post_valid_form(self):
        response = self.client.post(reverse('compiler:register'), data={
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'testuser')
    
    def test_register_view_post_invalid_form(self):
        response = self.client.post(reverse('compiler:register'), data={
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/register.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)
    
    def test_user_login_view_get(self):
        response = self.client.get(reverse('compiler:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/login.html')
        self.assertIsNone(response.context['error_message'])
        self.assertContains(response, 'Login')
    
    def test_user_login_view_post_invalid_credentials(self):
        response = self.client.post(reverse('compiler:login'), data={
            'username': 'testuser',
            'password': 'invalidpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/login.html')
        self.assertEqual(response.context['error_message'], 'Invalid username or password.')
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_user_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('compiler:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('compiler:start'))
    
    def test_main_view_authenticated_user(self):
        user = User.objects.get(id=1)
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('compiler:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/index.html')
        
        Folder.objects.create(name='Folder 1', owner=user)
        Folder.objects.create(name='Folder 2', owner=user)
        File.objects.create(name='File 1', owner=user)
        
        response = self.client.get(reverse('compiler:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/index.html')
        self.assertEqual(len(response.context['folders']), 2)
        self.assertEqual(len(response.context['files']), 1)
        self.assertContains(response, 'Folder 1')
        self.assertContains(response, 'Folder 2')
        self.assertContains(response, 'File 1')
        
    def test_compiled_file_view_null_file(self):
        user = User.objects.get(id=1)
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('compiler:compiledFile', args=["null", 'std', 'opt', 'proc', 'dep']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/noFileSelected.html')
    
    def test_new_folder_view_get(self):
        user = User.objects.get(id=1)
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('compiler:newFolder'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/newFolder.html')
        self.assertIsInstance(response.context['form'], FolderForm)
    
    def test_new_folder_view_post_valid_form(self):
        user = User.objects.get(id=1)
        self.client.login(username='testuser', password='testpassword')
        
        data = {'name': 'Test Folder'}
        response = self.client.post(reverse('compiler:newFolder'), data=data)
        self.assertRedirects(response, reverse('compiler:main'))
        
        folders = Folder.objects.filter(owner=user)
        self.assertEqual(len(folders), 1)
        self.assertEqual(folders[0].name, 'Test Folder')
    
    def test_delete_file_view_get(self):
        user = User.objects.get(id=1)
        self.client.login(username='testuser', password='testpassword')
        
        file = File.objects.create(name='Test File', owner=user)
        
        response = self.client.get(reverse('compiler:deleteFile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/deleteFile.html')
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_start_view(self):
        response = self.client.get(reverse('compiler:start'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/start.html')

    def test_register_view(self):
        response = self.client.get(reverse('compiler:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/register.html')

    def test_user_login_view(self):
        response = self.client.get(reverse('compiler:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/login.html')

    def test_user_logout_view(self):
        response = self.client.get(reverse('compiler:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('compiler:start'))

    def test_MainView(self):
        response = self.client.get(reverse('compiler:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/index.html')

    def test_ShowingFileView(self):
        file = File.objects.create(name='Test File', owner=self.user, upload=file_upload)
        response = self.client.get(reverse('compiler:showingFile', args=[file.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/showFile.html')

    def test_CompiledFileView_no_file_selected(self):
        response = self.client.get(reverse('compiler:compiledFile', args=["null", "null", "null", "null", "null"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/noFileSelected.html')

    def test_CompiledFileView_with_file_selected(self):
        file = File.objects.create(name='testfile', owner=self.user)
        response = self.client.get(reverse('compiler:compiledFile', args=[file.id, "null", "null", "null", "null"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/showCompiled.html')

    def test_NewFolderView(self):
        response = self.client.get(reverse('compiler:newFolder'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/newFolder.html')

    def test_NewFileView(self):
        response = self.client.get(reverse('compiler:newFile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/newFile.html')

    def test_DeleteFolderView(self):
        response = self.client.get(reverse('compiler:deleteFolder'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/deleteFolder.html')

    def test_DeleteFileView(self):
        response = self.client.get(reverse('compiler:deleteFile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/deleteFile.html')

    def test_NewSectionView(self):
        response = self.client.get(reverse('compiler:newSection'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compiler/newSection.html')
