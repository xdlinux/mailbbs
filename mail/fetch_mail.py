#!/usr/bin/env python2
# -*- coding:utf8 -*-
import poplib
import string
from models import Mail


def fetch_mail():
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
	return True

		
