from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.


def index(request):
    request.session.flush()
    return render(request, 'index.html')


def register(request):
    if request.method != "POST":
        return redirect('/')
    errors = User.objects.register_validator(request.POST)
    # Validation
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    hashed_pw = bcrypt.hashpw(
        request.POST['pwd'].encode(), bcrypt.gensalt()).decode()

    # Create a new user in the database
    new_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        pwd=hashed_pw
    )

    # Store the user's ID in the request.session
    request.session['user_id'] = new_user.id
    return redirect('/dashboard')


def login(request):
    if request.method != "POST":
        return redirect('/')

    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    # find the user trying to login

    this_user = User.objects.filter(email=request.POST['email'])[0]
    # put the user id in request.session

    request.session['user_id'] = this_user.id

    messages.success(
        request, "Success! Welcome, you're logged in!")
    return redirect('/dashboard')


def dashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, "You have to login to see that page")
        return redirect('/')
    this_user = User.objects.get(id=request.session['user_id']) 

    
    context = {

        'this_user': User.objects.get(id=request.session['user_id']),
        'all_jobs': Job.objects.all(),
        'fave_jobs' : this_user.favorite_jobs.all(),
    }

    return render(request, 'dashboard.html', context)

def new_job(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {

        'this_user': User.objects.get(id=request.session['user_id']),
    
    }

    return render(request, 'jobs.html', context)

def create(request):
    if 'user_id' not in request.session:
        return redirect('/')


    this_user = User.objects.get(id = request.session['user_id'])

    errors = Job.objects.job_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/new')
    else: 
        Job.objects.create(
            title = request.POST['ttl'], 
            dsc = request.POST['dsc'], 
            lctn = request.POST['lctn'], 
            posted_by=this_user)
    return redirect('/dashboard')

def edit_job(request, job_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_job = Job.objects.get(id=job_id)
    this_user = User.objects.get(id= request.session['user_id'])

    authorized_user = this_job.posted_by.id 

    if this_user.id == authorized_user:
        context = {
            'job_to_edit': this_job,
            'user' : this_user,
        }
        return render(request, 'edit_job.html', context)

    else:
        return redirect('/dashboard')


def update_job(request, job_id):
    if request.method != 'POST' or 'user_id' not in request.session:
        return redirect('/')

    this_job = Job.objects.get(id=job_id)
    this_user = User.objects.get(id = request.session['user_id'])

    errors = Job.objects.job_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/{this_job.id}/edit")
    else:
        this_job.title = request.POST['ttl']
        this_job.dsc = request.POST['dsc']
        this_job.lctn = request.POST['lctn']
        this_job.save()
    return redirect('/dashboard')

def delete_job(request, job_id):
    if request.method != 'POST' or 'user_id' not in request.session:
        return redirect('/')

    this_job = Job.objects.get(id= job_id)
    this_job.delete()
    return redirect('/dashboard')

def favorites(request, job_id, user_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_job = Job.objects.get(id= job_id)
    this_user = User.objects.get(id = user_id)
    this_user.favorite_jobs.add(this_job)
    return redirect('/dashboard')

def unfavorite(request, fave_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_job = Job.objects.get(id= fave_id)
    this_user = User.objects.get(id = request.session['user_id'])
    this_user.favorite_jobs.remove(this_job)
    return redirect('/dashboard')


def job_profile(request, job_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    this_user = User.objects.get(id = request.session['user_id'])
    job = Job.objects.get(id = job_id)
    

    context = {
        'user' : this_user,
        'this_job' : job,
        'fave_jobs' : this_user.favorite_jobs.all(),
    }
    return render(request, 'job_profile.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')
