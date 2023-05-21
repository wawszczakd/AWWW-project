from django.urls import path
from . import views

app_name = 'compiler'
urlpatterns = [
	path('main/', views.MainView, name='main'),
	path('main/file/<int:file_id>/', views.ShowingFileView, name='showingFile'),
	path('main/file/<int:file_id>/compiled/', views.CompiledFileView, name='compiledFile'),
	path('main/file/<int:file_id>/compiled/download/', views.DownloadCompiledView, name='downloadCompiled'),
	path('main/newFolder/', views.NewFolderView, name='newFolder'),
	path('main/newFile/', views.NewFileView, name='newFile'),
	path('main/deleteFolder/', views.DeleteFolderView, name='deleteFolder'),
	path('main/deleteFile/', views.DeleteFileView, name='deleteFile'),
]