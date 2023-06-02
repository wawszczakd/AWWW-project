from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils import timezone
from django.http import  FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import subprocess
import os, io, re

def start(request):
	return render(request, 'compiler/start.html')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('compiler:login')
	else:
		form = UserCreationForm()
	return render(request, 'compiler/register.html', {'form': form})

def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('compiler:main')
		else:
			error_message = "Invalid username or password."
	else:
		error_message = None
	return render(request, 'compiler/login.html', {'error_message': error_message})

@login_required
def user_logout(request):
    logout(request)
    return redirect('compiler:start')

@login_required
def MainView(request):
	context = {
		'folders'      : Folder.objects.filter(parent__isnull = True, isAvailable = True, owner=request.user),
		'files'        : File.objects.filter(folder__isnull = True, isAvailable = True, owner=request.user),
	}
	return render(request, 'compiler/index.html', context)

@login_required
def ShowingFileView(request, file_id):
	file = get_object_or_404(File, id = file_id)
	
	request.session['file_name'] = None
	request.session['asm_path'] = None
	request.session['asm_to_show'] = None
	request.session['err'] = None
	
	return render(request, 'compiler/showFile.html', {'file_to_show' : file.upload.open('r').read()})

@login_required
def CompiledFileView(request, file_id, standard, optimization, processor, dependent):
	if file_id == "null":
		return render(request, 'compiler/noFileSelected.html')
	file_id = int(file_id)
	
	file = get_object_or_404(File, id = file_id)
	file_name = os.path.basename(file.upload.name)
	
	command = ['sdcc', '-S']
	
	if standard != "null":
		standard = f'--std-{standard}'
		command.append(standard)
	
	if optimization != "null":
		optimization = f'--{optimization}'
		command.append(optimization)
	
	if processor != "null":
		processor = f'-m{processor}'
		command.append(processor)
	
	if dependent != "null":
		if dependent in ["small", "medium", "large"]:
			dependent = f'--model-{dependent}'
		else:
			dependent = f'--asm={dependent}'
		command.append(dependent)
	
	command.append(file_name)
	
	result = subprocess.run(command, capture_output=True, text=True)
	err = result.stderr
	asm_path = None
	compiled = None
	sections = None
	
	if not err:
		asm_path = os.path.join(os.getcwd(), file_name.rsplit('.', 1)[0] + '.asm')
		with open(asm_path, 'r') as fasm:
			compiled = fasm.read()
		
		sections = re.split(';--+', compiled)
	
	request.session['file_name'] = file.name
	request.session['asm_path'] = asm_path
	request.session['err'] = err
	request.session['asm_to_show'] = compiled
	
	return render(request, 'compiler/showCompiled.html', {'err' : err, 'sections' : sections})

@login_required
def DownloadCompiledView(request):
	asm_path = request.session['asm_path']
	content = request.session['asm_to_show']
	filename = os.path.splitext(request.session['file_name'])[0] + '.asm'
	
	file_obj = io.BytesIO(content.encode('utf-8'))
	response = FileResponse(file_obj)
	response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
	
	return response

@login_required
def NewFolderView(request):
	context = {
		'current_date' : timezone.now().strftime("%Y-%m-%d %H:%M"),
		'folders'      : Folder.objects.filter(isAvailable = True, owner=request.user),
	}
	
	if request.method != "POST":
		form = FolderForm()
		context['form'] = form
		return render(request, 'compiler/newFolder.html', context)
	
	form = FolderForm(request.POST)
	
	if form.is_valid():
		folder = form.save(commit=False)
		folder.owner = request.user
		folder.save()
		return redirect('compiler:main')
	
	form = FolderForm()
	context['form'] = form
	return render(request, 'compiler/newFolder.html', context)

@login_required
def NewFileView(request):
	context = {
		'folders'      : Folder.objects.filter(isAvailable = True, owner=request.user),
	}
	
	if request.method != "POST":
		form = FileForm()
		context['form'] = form
		return render(request, 'compiler/newFile.html', context)
	
	form = FileForm(request.POST, request.FILES)
	
	if form.is_valid():
		file = form.save(commit=False)
		file.owner = request.user
		file.save()
		
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

@login_required
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

@login_required
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

@login_required
def NewSectionView(request):
	context = {
		'files' : File.objects.filter(isAvailable = True, owner=request.user),
	}
	
	if request.method != "POST":
		form = SectionForm()
		context['form'] = form
		return render(request, 'compiler/newSection.html', context)
	
	form = SectionForm(request.POST, request.FILES)
	
	if form.is_valid():
		section = form.save(commit=False)
		section.owner = request.user
		section.save()
		
		return redirect('compiler:main')
	
	form = SectionForm()
	context['form'] = form
	return render(request, 'compiler/newSection.html', context)