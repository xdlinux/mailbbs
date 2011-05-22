# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,get_object_or_404

import poplib
import string
from models import Mail


def fetch_mail(request):
	"""docstring for fetch_mail"""
	p=poplib.POP3('pop3.163.com')
	p.user('airobot1')
	p.pass_('ragamuffin')
	count,size=p.stat()
	for i in range(count):
		hr,msg,oct=p.retr(i+1)
		mail=Mail()
		mail.RawData=string.join(msg,'\n')
		mail.save()
	return HttpResponseRedirect('/admin/')

def index(request):
	"""docstring for index"""
	mails=Mail.objects.filter(InReplyToRoot=None).order_by('-Datetime')[:10]
	return render_to_response('mail_list.html',locals())
def detail(request,mail_id):
	"""docstring for detail"""
	mail=get_object_or_404(Mail,id=mail_id)
	return render_to_response('mail_detail.html',locals())
