from django.shortcuts import render,get_object_or_404
from .models import Project
from submission.models import Submission
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView,DetailView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#Called to Get the Details of a Project.
# This can be accessed from the feed.

@login_required
def details(request,project_id) :
    current_project=get_object_or_404(Project,pk=project_id)
    context ={'project' : current_project,"sameuser": str(request.user)==current_project.creator}
    return render(request,'projects/details.html',context)

#This is not a view

@login_required
def create_submission_in_correct_format(request,project_id) :
    '''
        Create a Submission Object
    '''
    sub = Submission()
    sub.submitter = str(request.user)
    sub.files = request.POST["files"]
    sub.dateTimeField = timezone.now()
    sub.project = project_id
    sub.rank = 0
    return sub

# This is the form the user has to fill to create a new project

@login_required
def create_project_form(request):
    '''Loads the template html to create project'''
    return render(request, 'projects/create_project.html')

# The is called from the form.
# After completion the user is redirected to the create_project html
def create_project(request):
    ''' Accepts a request from the form in create_project
        and creates the project object '''
    name= request.POST["project_name"]
    desc= request.POST["project_description"]
    amount= request.POST["amount"]
    date= request.POST["datetime"]
    level = request.POST['level']
    username=request.user
    try :
        p = Project(name=name,level=level,amount=amount,creator=username,description=desc,deadline=date,date_posted=timezone.now(),ranked=False)
    except() :
        return render(request,"polls/create_project.html",{error:"Incorrect Values provided"})

    else :
        p.save()
        return HttpResponseRedirect(reverse("projects:details",args={p.id}))

    return render(request,'projects/create_project.html')

# This is called by a submitter who is going to upload his files onto the project. It is redirected to the same project html page
@login_required
def make_submission(request,project_id) :
    project = get_object_or_404(Project,pk=project_id)
    #TODO Need to add submission to user profile too
    #TODO Check if username exists
    current_submissions = project.submissions
    # If at least one submission has been made
    if(current_submissions is not None) :
        # If a the same user has made a submission
        for i,sub in enumerate(current_submissions):
            if sub.submitter ==  str(request.user):
                current_submissions.pop(i)
                current_submissions.append(create_submission_in_correct_format(request,project_id))
                break;
        else :
        # If a the same user has not made a submission
            current_submissions.append(create_submission_in_correct_format(request,project_id))

    else :
    # If no submissions made at all
        current_submissions =[create_submission_in_correct_format(request,project_id)]


    project.submissions = current_submissions
    project.save()
    return HttpResponseRedirect(reverse("projects:details",args=(project_id,)))

# The Creator of the project can set the rank of the submissions.
@login_required
def set_ranks(request,project_id) :
    project = get_object_or_404(Project,pk=project_id)
    submissions = project.submissions
    User =  get_user_model()
    for sub in submissions :
        val=request.POST["rank"+sub.submitter]
        if(val=="") :
            sub.rank=0
        else :
            sub.rank=val
            submitter = User.objects.get(username=sub.submitter)
            submitter.increment_score(project.level,int(val))
            submitter.save()
    project.ranked=True
    project.save()
    return HttpResponseRedirect(reverse("projects:details",args=(project_id,)))


class project_list_view(ListView):
    model=Project
    template_name='projects/home.html'
    context_object_name='projects'
    ordering=['-date_posted']

