from django.conf.urls.defaults import patterns,url
from mailbbs.mail.views import fetch_mail

urlpatterns=patterns('',
		url(r'^fetch_mail/$',fetch_mail),
		)
