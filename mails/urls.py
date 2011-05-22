from django.conf.urls.defaults import patterns,url
from mailbbs.mails.views import *

urlpatterns=patterns('',
		url(r'^$',index),
		url(r'^(\d+)$',detail),
		url(r'^fetch_mail/$',fetch_mail),
		)
