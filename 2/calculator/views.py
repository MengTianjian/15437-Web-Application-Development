# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def validate_request(request):
	if 'lastinput' in request.POST:
		if request.POST['lastinput'] != 'digit' and request.POST['lastinput'] != 'operator':
			return False
	if 'lastdisplay' in request.POST:
		if request.POST['lastdisplay'] != 'error' and request.POST['lastdisplay'] != 'invalid input' and not check_int(request.POST['lastdisplay']):
			return False
	if 'lastdigit' in request.POST:
		if not check_int(request.POST['lastdigit']):
			return False
	if 'lastoperator' in request.POST:
		if request.POST['lastoperator'] != '=' and request.POST['lastoperator'] != '+' and request.POST['lastoperator'] != '-' and request.POST['lastoperator'] != '*' and request.POST['lastoperator'] != '/':
			return False
	if 'digit' in request.POST:
		if 'operator' in request.POST or not check_int(request.POST['digit']):
			return False
		elif check_int(request.POST['digit']):
			if int(request.POST['digit']) < 0 or int(request.POST['digit']) > 9:
				return False
	if 'operator' in request.POST:
		if 'digit' in request.POST:
			return False
		elif request.POST['operator'] != '=' and request.POST['operator'] != '+' and request.POST['operator'] != '-' and request.POST['operator'] != '*' and request.POST['operator'] != '/':
			return False
	return True


# Create your views here.
def index(request):
	context = {}
	context['display'] = '0'
	context['digit'] = '0'

	if not validate_request(request):
		context['display'] = 'invalid input'
		return render(request, 'index.html', context)

	if 'lastinput' in request.POST:
		if 'digit' in request.POST:
			if request.POST['lastinput'] == 'digit':
				context['display'] = int(request.POST['lastdisplay']) * 10
				context['display'] = context['display'] + int(request.POST['digit'])
			elif request.POST['lastinput'] == 'operator':
				context['display'] = request.POST['digit']
			if 'lastoperator' in request.POST:
				context['operator'] = request.POST['lastoperator']
			if 'lastdigit' in request.POST:
				context['digit'] = request.POST['lastdigit']
			context['lastinput'] = 'digit'
		elif 'operator' in request.POST:
			if request.POST['lastinput'] == 'operator':
				if 'lastdisplay' in request.POST:
					context['display'] = request.POST['lastdisplay']
				context['operator'] = request.POST['operator']
				if 'lastdigit' in request.POST:
					context['digit'] = request.POST['lastdigit']
			elif request.POST['lastinput'] == 'digit':
				if 'lastoperator' in request.POST:
					if request.POST['lastoperator'] == "+":
						context['display'] = int(request.POST['lastdigit']) + int(request.POST['lastdisplay'])
					elif request.POST['lastoperator'] == "-":
						context['display'] = int(request.POST['lastdigit']) - int(request.POST['lastdisplay'])
					elif request.POST['lastoperator'] == "*":
						context['display'] = int(request.POST['lastdigit']) * int(request.POST['lastdisplay'])
					elif request.POST['lastoperator'] == "/":
						if int(request.POST['lastdisplay']) == 0:
							context['display'] = 'error'
						else:
							context['display'] = int(request.POST['lastdigit']) / int(request.POST['lastdisplay'])
					context['operator'] = request.POST['operator']
					if request.POST['lastoperator'] != "=":
						context['digit'] = context['display']
					else:
						context['display'] = request.POST['lastdisplay']
						context['digit'] = request.POST['lastdisplay']
				else:
					context['display'] = request.POST['lastdisplay']
					context['operator'] = request.POST['operator']
					context['digit'] = request.POST['lastdisplay']
			context['lastinput'] = 'operator'
	else:
		if 'digit' in request.POST:
			context['display'] = request.POST['digit']
			context['lastinput'] = 'digit'
		elif 'operator' in request.POST:
			context['operator'] = request.POST['operator']
			context['lastinput'] = 'operator'
	if context['display'] == 'error':
		context['digit'] = '0'
	return render(request, 'index.html', context)
