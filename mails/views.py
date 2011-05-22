# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,get_object_or_404

import poplib,smtplib,string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from models import Mail
from forms import ReplyForm


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
		p.dele(i+1)
	p.quit()
	return HttpResponseRedirect('/admin/')

def send_mail(tmail,form):
	"""docstring for send_mail"""
	msg=MIMEMultipart()
	msg['From']="%s <airobot1@163.com>" % form.cleaned_data['Name']
	msg['To']="airobot1@163.com" 
	msg['Subject']=tmail.Subject
	msg['In-Reply-To']=tmail.InReplyToRoot.MessageId
	msg['Direct-In-Reply-To']=tmail.MessageId
	msg.attach(MIMEText(form.cleaned_data['Content']))
	
	smtp=smtplib.SMTP()
	smtp.connect("smtp.163.com")
	smtp.login('airobot1','ragamuffin')
	smtp.sendmail('airobot1@163.com','airobot1@163.com',msg.as_string())
	smtp.quit()

def reply(request,target_mail_id):
	"""docstring for send_mail"""
	tmail=get_object_or_404(Mail,id=target_mail_id)
	if request.POST:
		form=ReplyForm(request.POST)
		if form.is_valid():
			send_mail(tmail,form)
			return HttpResponseRedirect('/')
	else:
		form=ReplyForm()
	return render_to_response('reply.html',locals())

def index(request):
	"""docstring for index"""
	mails=Mail.objects.filter(InReplyToRoot=None).order_by('-Datetime')[:10]
	return render_to_response('mail_list.html',locals())
def detail(request,mail_id):
	"""docstring for detail"""
	mail=get_object_or_404(Mail,id=mail_id)
	return render_to_response('mail_detail.html',locals())
