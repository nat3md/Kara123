from django.shortcuts import render, redirect
from .models import User, Job
from django.contrib import messages
import bcrypt

#Login & Registration
def index(request):
    return render(request, 'index.html')

def display_dashboard(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id=request.session['uuid']),
        "jobs": Job.objects.all(),
        'user_jobs': Job.objects.filter(first_name=User.objects.get(id=request.session['uuid']))
    }
    print(Job.objects.all())
    return render(request, 'dashboard.html', context)

def register_user(request):
    print(request.POST)
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hash_browns = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hash_browns)


    created_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hash_browns
)

    request.session['uuid'] = created_user.id
    return redirect('/dashboard')

def login_user(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['uuid'] = user.id
    return redirect('/dashboard')

def logout_user(request):
    request.session.flush()
    return redirect('/')

def jobs(request):
    print(request.POST)
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/new')

    created_job = Job.objects.create(
        title=request.POST['title'],
        description=request.POST['description'],
        location=request.POST['location'],
        first_name=User.objects.get(id=request.session['uuid']))
    return redirect('/dashboard')

def new_job(request):
    context = {
        'user' : User.objects.get(id=request.session['uuid'])
    }
    return render(request, 'jobs.html', context)

def jobs_int(request, job_id):
    print(request.GET)
    context = {
        "job": Job.objects.get(id=job_id),
        'user' : User.objects.get(id=request.session['uuid'])
    }
    return render(request, 'jobs_int.html', context)

def job_edit(request, job_id):
    print(request.POST)
    Job.objects.create(
        title=request.POST["title"],
        description=request.POST["description"],
        location=request.POST['location'])
    return redirect(request, 'job_edit.html')

def job_render(request, job_id):
    context = {
        'current_job': Job.objects.get(id=job_id),
        'user' : User.objects.get(id=request.session['uuid'])
    }
    return render(request, 'edit_job.html', context)

def update_job(request, job_id):
    print(request.POST)
    updated_job = Job.objects.get(id=job_id)
    updated_job.title=request.POST['title']
    updated_job.description=request.POST['description']
    updated_job.location=request.POST['location']
    updated_job.save()
    return redirect('/dashboard')

def delete_job(request, job_id):
    print(request.POST)
    delete_job = Job.objects.get(id=job_id)
    delete_job.delete()
    return redirect('/dashboard')