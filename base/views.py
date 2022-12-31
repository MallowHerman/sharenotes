from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import mimetypes
import os
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Document, Category, Subject, School, Course
from django.db.models import Q
from .forms import DocumentForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .utils import convert_pdf_to_image

def index(request):
    return render(request, 'base/index.html')

def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    documents = Document.objects.filter(Q(name__icontains=q) | Q(course__name__icontains=q))

    context = {
        'documents': documents,
    }
    return render(request, 'base/search.html', context)

def documentDetailView(request, slug, pk):
    document = Document.objects.get(slug=slug, id=pk)
    user = User.objects.get(id=document.author.pk)
    context = {
        'document': document,
        'user': user
    }
    return render(request, 'base/document_detail.html', context)

@login_required
def upload_document(request):
    document_types = Category.objects.all()
    subjects = Subject.objects.all()
    schools = School.objects.all()
    courses = Course.objects.all()
    if request.method == 'POST':
        subject, created = Subject.objects.get_or_create(name=request.POST.get('subject'))
        school, created = School.objects.get_or_create(name=request.POST.get('school'))
        course, created = Course.objects.get_or_create(name=request.POST.get('course'))
        document_type, created = Category.objects.get_or_create(name=request.POST.get('document_type'))

        save_document = Document.objects.create(
            name = request.POST.get('name'),
            description = request.POST.get('description'), 
            course = course,
            school = school,
            subject = subject,
            category = document_type,
            document = request.FILES['document'],
            author = request.user
        )

        thumbnail = convert_pdf_to_image(save_document.document.url, save_document.document)
        print(thumbnail[0])

        return redirect('base:index')
        
    context = {
        'document_types': document_types,
        'subjects': subjects,
        'schools': schools,
        'courses': courses
    }
    return render(request, 'base/upload_document.html', context)



@login_required
def download_file(request, filename):
    filename = filename
    if filename != '':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + '/media/' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        document = get_object_or_404(Document, id=request.POST.get('document_id'))
        document.downloads.add(request.user)

        return response
    else:
        # Load the template
        return render(request, 'base/download.html')

@login_required
def documentLike(request, pk):
    document = get_object_or_404(Document, id=request.POST.get('document_id'))
    if document.likes.filter(id=request.user.id).exists():
        document.likes.remove(request.user)
    else:
        document.likes.add(request.user)

    return HttpResponseRedirect(reverse('base:document_detail', args=[str(document.slug) ,str(pk)]))