from django.db import models
import email
from datetime import datetime

def content(mail):
	"""docstring for content"""
	if mail.is_multipart():
		content(mail.get_payload()[1])
	else:
		charset=mail.get_content_charset()
		if type==None:
			return mail.get_payload(decode=True)
		try:
			return unicode(mail.get_payload(decode=True),type)
		except Exception, e:
			return mail.get_payload(decode=True)

# Create your models here.
class Mail(models.Model):
	"""docstring"""
	From = models.CharField(max_length=256)
	To = models.CharField(max_length=256)
	Subject = models.CharField(max_length=256)
	MessageId = models.CharField(max_length=256)
	Content = models.TextField()
	InReplyTo = models.ForeignKey(Mail, related_name='FollowingMails',null=True,blank=True)
	InReplyToRoot = models.ForeignKey(Mail, related_name='ChildMails',null=True,blank=True)
	RawData = models.TextField()
	Datetime = models.DateField()
	def __unicode__(self):
		return self.Subject
	def save(self, force_insert=False, force_update=False):
		mail=email.message_from_string(self.RawData)
		self.From=mail['From']
		self.To=mail['To']
		self.Subject=mail['Subject']
		self.MessageId=mail['Message-Id']
		self.Content=content(mail)
		self.Datetime=datetime.strptime(mail['Date'],'%a, %d %b %Y %H:%M:%S +0000')
		if mail['In-Reply-To']:
			try:
				self.InReplyTo=Mail.objects.get(MessageId=mail['In-Reply-To'])
			except:
				self.InReplyTo=None
			else:
				cmail=self.InReplyTo
				while cmail.InReplyTo:
					cmail=cmail.InReplyTo
				self.InReplyToRoot=cmail
		models.Model.save(self,force_insert,force_update)
	

