# Create your views here.
from django.http import HttpResponseRedirect

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

def send_mail(request):
	"""docstring for send_mail"""
	if request.POST:


		
