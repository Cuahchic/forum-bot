# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 20:55:54 2018

@author: colin
"""

from splinter import Browser


b = Browser()

b.visit('https://login.proboards.com/login/5738203/1')

b.fill('email', '')
b.fill('password', '')

b.find_by_name('continue').click()

b.html
b.find_by_css('post')