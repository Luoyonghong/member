# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^statics/(?P<path>.*)','django.views.static.serve',{'document_root':'member/statics'}), 
    # Examples:
    url(r'^$', 'member.views.login', name='home'),
    # url(r'^testzzq/', include('testzzq.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^reg$','member.views.reg'),
    url(r'^login$','member.views.login'),
    url(r'^index$','member.views.index'),
    url(r'^depart/(.+)/$','member.views.depart'), # 各部门的信息
    url(r'^reg_result/$','member.views.reg_result'),
    url(r'^reg_result/index/$','member.views.index'),
    url(r'^login_result/$','member.views.login_result'),
    url(r'^index/(.+)/$','member.views.index_of_others'),# 其他人的详细信息
    url(r'^edit$','member.views.edit'),
    url(r'^edit_result/$','member.views.edit_result'),
    url(r'^logout$','member.views.logout'),
                       
)
