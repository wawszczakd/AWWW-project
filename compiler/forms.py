from django import forms

from compiler.models import *

class FolderForm(forms.ModelForm):
	class Meta:
		model = Folder
		fields = [
			"parent",
			"name",
			"description",
		]

class DeleteFolderForm(forms.ModelForm):
	class Meta:
		model = Folder
		fields = [
			"parent",
		]

class FileForm(forms.ModelForm):
	class Meta:
		model = File
		fields = [
			"upload",
			"folder",
			"name",
			"description",
		]

class DeleteFileForm(forms.ModelForm):
	class Meta:
		model = FileToDelete
		fields = [
			"file",
		]

class SectionForm(forms.ModelForm):
	class Meta:
		model = Section
		fields = [
			"file",
			"name",
			"description",
			"beginning",
			"ending",
		]