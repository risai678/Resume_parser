from django.shortcuts import render, redirect
from pyresparser import ResumeParser
from .models import Resume, UploadResumeModelForm
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, FileResponse, Http404
import os
from docx2pdf import convert

def homepage(request):
    if request.method == 'POST':
        Resume.objects.all().delete()
        file_form = UploadResumeModelForm(request.POST, request.FILES)
        print(file_form, 'fffffff')
        files = request.FILES.getlist('resume')
        resumes_data = []

        if file_form.is_valid():
            for file in files:

                try:
                    print(file,'uuuuu')
                    # saving the file
                    # file=convert(str(file))
                    resume = Resume(resume=file)
                    resume.save()
                    
                    # extracting resume entities
                    # print(os.path.join(settings.MEDIA_ROOT, resume.resume.name),'firrrrrr')
                    # if str(file).split('.')[-1]=='doc' or str(file).split('.')[-1]=='docx':
                    #     new_file=resume.resume.name.split('.')[0]+'.pdf'
                    #     print(os.path.join(settings.MEDIA_ROOT, resume.resume.name),'dddddd')
                    #     print(os.path.join(settings.MEDIA_ROOT, new_file) ,'pddff')
                    #     convert(os.path.join(settings.MEDIA_ROOT, resume.resume.name),os.path.join(settings.MEDIA_ROOT, new_file) )
                        # file = convert(os.path.join(settings.MEDIA_ROOT, resume.resume.name))

                    parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
                    print(parser,'ggggg')
                    data = parser.get_extracted_data()
                    resumes_data.append(data)
                    resume.name               = data.get('name')
                    resume.email              = data.get('email')
                    resume.mobile_number      = data.get('mobile_number')
                    if data.get('degree') is not None:
                        resume.education      = ', '.join(data.get('degree'))
                    else:
                        resume.education      = None
                    resume.company_names      = data.get('company_names')
                    resume.college_name       = data.get('college_name')
                    resume.designation        = data.get('designation')
                    resume.total_experience   = data.get('total_experience')
                    if data.get('skills') is not None:
                        resume.skills         = ', '.join(data.get('skills'))
                    else:
                        resume.skills         = None
                    if data.get('experience') is not None:
                        resume.experience     = ', '.join(data.get('experience'))
                    else:
                        resume.experience     = None
                    resume.save()
                except IntegrityError:
                    messages.warning(request, 'Duplicate resume found:', file.name)
                    return redirect('homepage')
            resumes = Resume.objects.all()
            messages.success(request, 'Resumes uploaded!')
            context = {
                'resumes': resumes,
            }
            return render(request, 'base.html', context)
    else:
        form = UploadResumeModelForm()
    return render(request, 'base.html', {'form': form})