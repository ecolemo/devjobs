# coding: utf8
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from djangobp.textutil import gettext
from django.core.exceptions import ValidationError

class ValidatedNumberField(models.IntegerField):
    def get_prep_value(self, value):
        try:
            return models.IntegerField.get_prep_value(self, value)
        except:
            raise ValidationError({self.name : [gettext('%s should be a number.') % gettext(self.verbose_name)]})

class Skill(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __unicode__(self):
        return self.name

class JobSeeker(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField()
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    pay_period = models.CharField(max_length=100)
    pay_currency = models.CharField(max_length=100)
    pay_amount = ValidatedNumberField()
    worktime = models.CharField(max_length=100)
    contract = models.CharField(max_length=100)
    location_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    skill_set = models.ManyToManyField(Skill)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, default='open')
    
    def location_text(self):
        if self.location_type == 'local':
            return gettext(self.location_type) % self.location
        else:
            return gettext(self.location_type)
        
    def pay_text(self):
        print self.pay_period, gettext(self.pay_period), self.pay_amount
        print gettext(self.pay_period) % self.pay_amount
        return (gettext(self.pay_period) % self.pay_amount) + '원'


    
