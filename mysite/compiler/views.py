from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils import timezone
from django.http import  FileResponse
from .models import Folder, File, User, Section
from .forms import FolderForm, FileForm, DeleteFolderForm, DeleteFileForm
import subprocess
import os, io, re

def MainView(request):
	context = {
		'folders'      : Folder.objects.filter(parent__isnull = True, isAvailable = True),
		'files'        : File.objects.filter(folder__isnull = True, isAvailable = True),
		'file_id'      : None,
		'file_to_show' : None,
		'asm_to_show'  : None,
		'asm_path'     : None,
	}
	return render(request, 'compiler/index.html', context)

def ShowingFileView(request, file_id):
	file = get_object_or_404(File, id = file_id)
	
	context = {
		'folders'      : Folder.objects.filter(parent__isnull = True, isAvailable = True),
		'files'        : File.objects.filter(folder__isnull = True, isAvailable = True),
		'file_id'      : file_id,
		'file_to_show' : file.upload.open('r').read(),
		'asm_to_show'  : None,
		'asm_path'     : None,
	}
	
	return render(request, 'compiler/index.html', context)

def CompiledFileView(request, file_id):
	file = get_object_or_404(File, id = file_id)
	
	file_name = os.path.basename(file.upload.name)
	
	standard = request.POST.get('standard')
	optimization = request.POST.get('optimization')
	processor = request.POST.get('processor')
	dependent = request.POST.get('dependent')
	
	command = ['sdcc', '-S']
	
	if standard:
		standard = f'--std-{standard}'
		command.append(standard)
	
	if optimization:
		optimization = f'--{optimization}'
		command.append(optimization)
	
	if processor:
		processor = f'-m{processor}'
		command.append(processor)
	
	if dependent:
		if dependent in ["small", "medium", "large"]:
			dependent = f'--model-{dependent}'
		else:
			dependent = f'--asm={dependent}'
		command.append(dependent)
	
	command.append(file_name)
	
	subprocess.run(command)
	
	asm_path = os.path.join(os.getcwd(), file_name.rsplit('.', 1)[0] + '.asm')
	with open(asm_path, 'r') as fasm:
		compiled = fasm.read()
	
	sections = re.split(';--+', compiled)
	
	request.session['sections'] = sections
	request.session['asm_to_show'] = compiled
	request.session['asm_path'] = asm_path
	
	context = {
		'folders'      : Folder.objects.filter(parent__isnull = True, isAvailable = True),
		'files'        : File.objects.filter(folder__isnull = True, isAvailable = True),
		'file_id'      : file_id,
		'file_to_show' : file.upload.open('r').read(),
		'asm_to_show'  : compiled,
		'asm_path'     : asm_path,
		'sections'     : sections,
	}
	
	return render(request, 'compiler/index.html', context)

def DownloadCompiledView(request, file_id):
	file = get_object_or_404(File, id = file_id)
	asm_path = request.session['asm_path']
	content = request.session['asm_to_show']
	filename = os.path.splitext(file.name)[0] + '.asm'
	
	file_obj = io.BytesIO(content.encode('utf-8'))
	response = FileResponse(file_obj)
	response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
	
	return response

def NewFolderView(request):
	context = {
		'current_date' : timezone.now().strftime("%Y-%m-%d %H:%M"),
		'folders'      : Folder.objects.filter(isAvailable = True),
		'users'        : User.objects.all()
	}
	
	if request.method != "POST":
		form = FolderForm()
		context['form'] = form
		return render(request, 'compiler/newFolder.html', context)
	
	form = FolderForm(request.POST)
	
	if form.is_valid():
		form.save()
		return redirect('compiler:main')
	
	form = FolderForm()
	context['form'] = form
	return render(request, 'compiler/newFolder.html', context)

def NewFileView(request):
	context = {
		'folders'      : Folder.objects.filter(isAvailable = True),
		'users'        : User.objects.all(),
	}
	
	if request.method != "POST":
		form = FileForm()
		context['form'] = form
		return render(request, 'compiler/newFile.html', context)
	
	form = FileForm(request.POST, request.FILES)
	
	if form.is_valid():
		form.save()
		
		text = form.cleaned_data['upload'].open('r').read().decode('utf-8')
		
		asm = re.findall('asm.*ednasm', text, re.DOTALL)
		dyr = re.findall('#.*\n', text)
		com = re.findall('\/\/.*\n', text) + re.findall('\/\*.*\*\/', text, re.DOTALL)
		dec = re.findall('.*=.*\n', text)
		pro = re.findall('\w*\(\)\s*{.*}', text, re.DOTALL)
		
		for x in asm:
			section = Section()
			tmp = text.index(x)
			section.beginning = text[:tmp].count('\n') + 1
			section.ending = section.beginning + x.count('\n')
			section.sectionType = 'inl'
			section.content = x
			section.file = File.objects.all().latest('id')
			section.save()
		
		for x in dyr:
			section = Section()
			tmp = text.index(x)
			section.beginning = text[:tmp].count('\n') + 1
			section.ending = section.beginning + x.count('\n')
			section.sectionType = 'dir'
			section.content = x
			section.file = File.objects.all().latest('id')
			section.save()
		
		for x in com:
			section = Section()
			tmp = text.index(x)
			section.beginning = text[:tmp].count('\n') + 1
			section.ending = section.beginning + x.count('\n')
			section.sectionType = 'com'
			section.content = x
			section.file = File.objects.all().latest('id')
			section.save()
		
		for x in dec:
			section = Section()
			tmp = text.index(x)
			section.beginning = text[:tmp].count('\n') + 1
			section.ending = section.beginning + x.count('\n')
			section.sectionType = 'dec'
			section.content = x
			section.file = File.objects.all().latest('id')
			section.save()
		
		for x in pro:
			section = Section()
			tmp = text.index(x)
			section.beginning = text[:tmp].count('\n') + 1
			section.ending = section.beginning + x.count('\n')
			section.sectionType = 'pro'
			section.content = x
			section.file = File.objects.all().latest('id')
			section.save()
		
		return redirect('compiler:main')
	
	form = FileForm()
	context['form'] = form
	return render(request, 'compiler/newFile.html', context)

def DeleteFolderView(request):
	context = {
		'folders' : Folder.objects.filter(isAvailable = True),
	}
	
	def deleteRecursive(folder):
		children = folder.getFolders()
		for child in children:
			deleteRecursive(child)
		Folder.objects.filter(id = folder.id).update(isAvailable = False)
		File.objects.filter(folder = folder).update(isAvailable = False)
	
	if request.method != "POST":
		form = DeleteFolderForm()
		context['form'] = form
		return render(request, 'compiler/deleteFolder.html', context)
	
	form = DeleteFolderForm(request.POST)
	
	if form.is_valid():
		deleteRecursive(form.cleaned_data['parent'])
		return redirect('compiler:main')
	
	form = DeleteFolderForm()
	context['form'] = form
	return render(request, 'compiler/deleteFolder.html', context)

def DeleteFileView(request):
	context = {
		'files' : File.objects.filter(isAvailable = True),
	}
	
	if request.method != "POST":
		form = DeleteFileForm()
		context['form'] = form
		return render(request, 'compiler/deleteFile.html', context)
	
	form = DeleteFileForm(request.POST)
	
	if form.is_valid():
		file = form.cleaned_data['file']
		File.objects.filter(id = file.id).update(isAvailable = False)
		return redirect('compiler:main')
	
	form = DeleteFileForm()
	context['form'] = form
	return render(request, 'compiler/deleteFile.html', context)