from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from djangobp.makohelper import render_to_response
from jobs.models import JobSeeker, Skill
import simplejson

class Form(object):
    
    def __init__(self, data):
        self.data = data
    
    def __getitem__(self, key):
        return self.data.get(key, '')
    
    def getlist(self, key):
        if 'getlist' in dir(self.data):
            return self.data.getlist(key, [])
        elif isinstance(self[key], list):
            return self[key]
        else:
            return []
    
    def checked(self, key, value):
        if self[key] == value:
            return 'checked="checked"'
        return ''

    def selected(self, key, value):
        if self[key] == value:
            return 'selected="selected"'
        return ''
        
def index(request, resource_id):
    if request.GET:
        request.form = Form(request.GET)
    else:
        request.form = Form({'pay_period':request.GET.get('pay_period', 'month'),
                             'pay_amount_min':request.GET.get('pay_amount_max', 0),
                             'pay_amount_min':request.GET.get('pay_amount_max', 0),
                             'search':request.GET.get('search', '')})

    objects = JobSeeker.objects.all()
        
    if request.form['skills']:
        for keyword in request.form['skills'].split(' '):
            if keyword:
                objects = objects.filter(skill_set__name__icontains=keyword)
    
    if 'title' in request.GET:
        print request.GET['title']
        objects = objects.filter(title__icontains=request.GET['title'])
        
    objects = objects.filter(status='open').order_by('-created')
    paginator = Paginator(objects, 20)
    pageobj = paginator.page(request.GET.get('page', 1))
    return render_to_response("jobseekers.html", locals())

@login_required
def new(request, resource_id):    
    csrf_token = csrf(request)['csrf_token']
    job_title_suggest = simplejson.dumps([obj['title'] for obj in JobSeeker.objects.values('title').distinct()])
    skill_suggest = simplejson.dumps([obj['name'] for obj in Skill.objects.values('name').distinct()])
    
    if not hasattr(request, 'form'):
        request.form = Form({'skill':[''], 'pay_period':'month'})
    return render_to_response("jobseeker_new.html", locals())

@login_required
def create(request, resource_id):
    try:
        data = {key: request.POST[key] for key in ['title', 'email', 'pay_period', 'pay_amount', 'pay_currency', 'worktime',
                                                   'contract', 'location_type', 'location', 'description']}
        jobseeker = JobSeeker(user=request.user, **data)
        jobseeker.full_clean()
        jobseeker.save()
        for skill_name in request.POST.getlist('skill'):
            if skill_name:
                skill, created = Skill.objects.get_or_create(name=skill_name)
                jobseeker.skill_set.add(skill)
        return HttpResponseRedirect('/jobseekers/%s' % jobseeker.id)
    
    except ValidationError as e:
        request.flash['ValidationError'] = {field:','.join(e.message_dict[field]) for field in e.message_dict}
        request.form = Form(request.POST)
        return new(request, resource_id)
    
def show(request, resource_id):
    jobseeker = JobSeeker.objects.get(id=resource_id)
    return render_to_response("jobseekers/show.html", locals())

    