from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, TweetView


urlpatterns = [
    url(r'^stanzas/$', CreateView.as_view(), name="create"),
    url(r'^tweet/$', TweetView, name='tweet')
]

urlpatterns = format_suffix_patterns(urlpatterns)
