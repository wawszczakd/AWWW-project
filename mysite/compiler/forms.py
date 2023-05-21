from django import forms

from compiler.models import Folder, File, FileToDelete

class FolderForm(forms.ModelForm):
	class Meta:
		model = Folder
		fields = [
			"parent",
			"name",
			"description",
			"owner",
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
			"owner",
		]

class DeleteFileForm(forms.ModelForm):
	class Meta:
		model = FileToDelete
		fields = [
			"file",
		]
