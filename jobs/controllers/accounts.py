from djangobp.makohelper import render_to_response
from social_auth.context_processors import social_auth_by_type_backends
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from jobs.models import JobSeeker
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def login(request, resource_id):
    csrf_token = csrf(request)['csrf_token']
    reverse_url = reverse
    l = locals()
    l.update(social_auth_by_type_backends(request))
    return render_to_response('login.html', l)

def logout(request, resource_id):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')

def show(request, resource_id):
    csrf_token = csrf(request)['csrf_token']
    objects = JobSeeker.objects.filter(user=request.user)
    return render_to_response("jobseekers/me.html", locals())    

@login_required
def action(request, resource_id):
    jobseeker = JobSeeker.objects.get(id=resource_id)
    if request.user.id != jobseeker.user.id:
        raise PermissionDenied()
    
    if request.POST['command'] == 'reopen':
        jobseeker.status ='open'
    elif request.POST['command'] == 'close':
        jobseeker.status ='closed'
    
    jobseeker.save()
    return HttpResponseRedirect('/accounts/me')

