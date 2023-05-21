from django.db import models

class Folder(models.Model):
	parent = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True)
	name = models.TextField()
	description = models.TextField(null=True, blank=True)
	creationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	owner = models.ForeignKey('User', on_delete=models.CASCADE, default = None, null=True, blank=True)
	isAvailable = models.BooleanField(default = True, null=True, blank=True)
	availableChangeDate = models.DateTimeField(null=True, blank=True)
	valueChangeDate = models.DateTimeField(auto_now=True, null=True, blank=True)
	
	def getFolders(self):
		return Folder.objects.filter(parent=self, isAvailable=True)
	
	def getFiles(self):
		return File.objects.filter(folder=self, isAvailable=True)

class File(models.Model):
	folder = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True)
	name = models.TextField()
	upload = models.FileField()
	description = models.TextField(null=True, blank=True)
	creationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	owner = models.ForeignKey('User', on_delete=models.CASCADE, default = None, null=True, blank=True)
	isAvailable = models.BooleanField(default = True, null=True, blank=True)
	availableChangeDate = models.DateTimeField(null=True, blank=True)
	valueChangeDate = models.DateTimeField(auto_now=True, null=True, blank=True)

class FileToDelete(models.Model):
	file = models.ForeignKey('File', on_delete=models.CASCADE, null=True, blank=True)

class FileSection(models.Model):
	name = models.TextField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	creationDate = models.DateTimeField()
	beginning = models.IntegerField()
	ending = models.IntegerField()
	sectionType = models.ForeignKey('SectionType', on_delete=models.CASCADE)
	sectionStatus = models.ForeignKey('SectionStatus', on_delete=models.CASCADE)
	dataStatus = models.ForeignKey('DataStatus', on_delete=models.CASCADE)
	content = models.TextField()

class SectionType(models.Model):
	content = models.TextField()

class SectionStatus(models.Model):
	content = models.TextField()

class DataStatus(models.Model):
	content = models.TextField()

class User(models.Model):
	name = models.TextField()
	login = models.TextField()
	password = models.TextField()
