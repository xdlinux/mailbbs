from django.db import models
import email
from datetime import datetime

def get_content(mail):
	"""docstring for content"""
	if mail.is_multipart():
		return get_content(mail.get_payload()[1])
	else:
		charset=mail.get_content_charset()
		if charset==None:
			return mail.get_payload(decode=True)
		try:
			return unicode(mail.get_payload(decode=True),charset)
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
	InReplyTo = models.ForeignKey('self', related_name='FollowingMails',null=True,blank=True)
	InReplyToRoot = models.ForeignKey('self', related_name='ChildMails',null=True,blank=True)
	RawData = models.TextField()
	Datetime = models.DateTimeField()
	def __unicode__(self):
		return self.Subject
	def save(self, force_insert=False, force_update=False):
		mail=email.message_from_string(self.RawData)
		codeset=email.Header.decode_header(mail['From'])[0][1]
		if codeset==None:
			codeset='ascii'
		self.From=unicode(email.Header.decode_header(mail['From'])[0][0],codeset)
		codeset=email.Header.decode_header(mail['To'])[0][1]
		if codeset==None:
			codeset='ascii'
		self.To=unicode(email.Header.decode_header(mail['To'])[0][0],codeset)
		codeset=email.Header.decode_header(mail['subject'])[0][1]
		if codeset==None:
			codeset='ascii'
		self.Subject=unicode(email.Header.decode_header(mail['Subject'])[0][0],codeset)
		self.MessageId=mail['Message-Id']
		self.Content=get_content(mail)
		self.Datetime=datetime.strptime(mail['Date'][:-6],'%a, %d %b %Y %H:%M:%S')

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
	

