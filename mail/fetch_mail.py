#!/usr/bin/env python2
# -*- coding:utf8 -*-
import poplib
import string

def fetch_mail():
	"""docstring for fetch_mail"""
	p=poplib.POP3('pop3.163.com')
	p.user('airobot1')
	p.pass_('ragamuffin')
	count,size=p.stat()
	for i in range(count):
		hr,msg,oct=p.retr(i)
		mail=email.message_from_string(string.join(msg,'\n'))
		
