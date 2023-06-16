from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
	parent = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True)
	name = models.TextField()
	description = models.TextField(null=True, blank=True)
	creationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default = None, null=True, blank=True)
	isAvailable = models.BooleanField(default = True, null=True, blank=True)
	availableChangeDate = models.DateTimeField(null=True, blank=True)
	valueChangeDate = models.DateTimeField(auto_now=True, null=True, blank=True)
	
	def getFolders(self):
		return Folder.objects.filter(parent=self, owner=self.owner, isAvailable=True)
	
	def getFiles(self):
		return File.objects.filter(folder=self, owner=self.owner, isAvailable=True)

class File(models.Model):
	folder = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True)
	name = models.TextField()
	upload = models.FileField()
	description = models.TextField(null=True, blank=True)
	creationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default = None, null=True, blank=True)
	isAvailable = models.BooleanField(default = True, null=True, blank=True)
	availableChangeDate = models.DateTimeField(null=True, blank=True)
	valueChangeDate = models.DateTimeField(auto_now=True, null=True, blank=True)

class FileToDelete(models.Model):
	file = models.ForeignKey('File', on_delete=models.CASCADE, null=True, blank=True)

SECTION_TYPE = (
	('pro', 'Procedura'),
	('com', 'Komentarz'),
	('dir', 'Dyrektywa'),
	('dec', 'Deklaracja'),
	('inl', 'Wstawka assemblerowa'),
)

SECTION_STATUS = (
	('ok', 'Kompiluje się bez ostrzeżeń'),
	('war', 'Kompiluje się z ostrzeżeniami'),
	('fail', 'Nie kompiluje się'),
)

class Section(models.Model):
	file = models.ForeignKey('File', on_delete=models.CASCADE, default=None, null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	parent = models.ForeignKey('Section', on_delete=models.CASCADE, default=None, null=True, blank=True)
	name = models.TextField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	creationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default = None, null=True, blank=True)
	beginning = models.IntegerField(null=True, blank=True)
	ending = models.IntegerField(null=True, blank=True)
	sectionType = models.TextField(choices=SECTION_TYPE, null=True, blank=True)
	sectionStatus = models.TextField(choices=SECTION_STATUS, null=True, blank=True)
