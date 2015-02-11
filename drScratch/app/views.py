#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpResponse, HttpResponseServerError
from django.core.context_processors import csrf
from django.core.cache import cache  
from django.shortcuts import render_to_response
from django.template import RequestContext as RC
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from app.models import AnonProject, AnonMastery
from app.models import Project, Dashboard, Attribute
from app.models import Dead, Sprite, Mastery, Duplicate, File
from app.forms import UserForm, NewUserForm, UrlForm
from datetime import datetime, date
import requests
import os
import ast
import json
import sys
import urllib2
import csv
import json

# Global variables
pMastery = "hairball -p mastery.Mastery "
pDuplicateScript = "hairball -p duplicate.DuplicateScripts " 
pSpriteNaming = "hairball -p convention.SpriteNaming "
pDeadCode = "hairball -p blocks.DeadCode "
pInitialization = "hairball -p initialization.AttributeInitialization "

#_______________________ MAIN _______________________________#

def main(request):
    """Main page"""
    if request.user.is_authenticated():
        user = request.user.username    
    else:
        user = None
    # The first time one user enters
    # Create the dashboards associated to users
    createDashboards()
    return render_to_response("main/main.html",
                                {'user':user},
                                context_instance=RC(request))

def redirectMain(request):
    """Page not found redirect to main"""
    return HttpResponseRedirect('/')

#________________________ REGISTRY __________________________#

def loginUser(request):
    """Log in app to user"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/myDashboard')
            else:
                flag = True
                return render_to_response("main/main.html", 
                                            {'flag': flag},
                                            context_instance=RC(request))

    else:
        return HttpResponseRedirect("/")


def logoutUser(request):
    """Method for logging out"""
    logout(request)
    return HttpResponseRedirect('/')

def createUser(request):
	"""Method for to sign up in the platform"""
	logout(request)
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			nickName = form.cleaned_data['nickname']
			emailUser = form.cleaned_data['emailUser']
			passUser = form.cleaned_data['passUser']
			user = User.objects.create_user(nickName, emailUser, passUser)
			return render_to_response("profile.html", {'user': user}, context_instance=RC(request))

#_________________________CSV File____________________________#
def exportCsvFile(request):
	"""Export a CSV File"""
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="some.csv"'
	d = {"Abstraction": 2, "level": " Developing", "Parallelization": 1, "Logic": 1, "Synchronization": 2, "FlowControl": 2, "UserInteractivity": 1, "maxPoints": 21, "DataRepresentation": 1, "points": 10}
	writer = csv.writer(response)
	for key, value in d.items():
   		writer.writerow([key, value])

	"""
	writer = csv.writer(response)
	writer.writerow(['First row', 'Paco', '21', 'Madrid'])
	writer.writerow(['Second row', 'Lucia', '25', 'Quito'])
	"""
	return response



#_________________________Drawing Blocks____________________________#


def drawBlocks(request):
	code = 'when backdrop switches to (%s)' + '\n' + 'go to x:(%s) y:(%s)' + '\n' + 'wait (%s) secs' + '\n' + 'show' + '\n' + 'glide (%s) secs to x:(%s) y:(%s)'
	return render_to_response("drawBlocks/drawBlocks.html", {'code': code})




#________________________ PROFILE ____________________________# 


def updateProfile(request):
	"""Update the pass, email and avatar"""
	if request.user.is_authenticated():
		user = request.user.username
	else:
		user = None
	if request.method == "POST":
		form = UpdateForm(request.POST)
		if form.is_valid():
			newPass = form.cleaned_data['newPass']
			newEmail = form.cleaned_data['newEmail']
			choiceField = forms.ChoiceField(widget=forms.RadioSelect())
			print newPass, newEmail, choiceField.widget.choices, choiceField
			return HttpResponseRedirect('/mydashboard')
		else:
			print 'movida'


def changePassword(request, new_password):
	"""Change the password of user"""
	user = User.objects.get(username=current_user)
	user.set_password(new_password)
	user.save()



#________________________ DASHBOARD ____________________________# 

def createDashboards():
    """Get users and create dashboards"""
    allUsers = User.objects.all()
    for user in allUsers:
        try:
            newdash = Dashboard.objects.get(user=user)
        except:
            fupdate = datetime.now()
            newDash = Dashboard(user=user.username, frelease=fupdate)
            newDash.save()
       
def myDashboard(request):
    """Dashboard page"""
    if request.user.is_authenticated():
        user = request.user.username
        # The main page of user
        # To obtain the dashboard associated to user
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        beginner = mydashboard.project_set.filter(level="beginner")
        developing = mydashboard.project_set.filter(level="developing")
        advanced = mydashboard.project_set.filter(level="advanced")
        return render_to_response("myDashboard/content-dashboard.html", 
                                    {'user': user,
                                    'beginner': beginner,
                                    'developing': developing,
                                    'advanced': advanced,
                                    'projects': projects},
                                    context_instance=RC(request))
    else:
        user = None
        return HttpResponseRedirect("/")

def myProjects(request):
    """Show all projects of dashboard"""
    if request.user.is_authenticated():
        user = request.user.username
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        return render_to_response("myProjects/content-myprojects.html", 
                                {'projects': projects,
								'user': user},
                                context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")
    
def myRoles(request):
    """Show the roles in Doctor Scratch"""
    if request.user.is_authenticated():
        user = request.user.username
        return render_to_response("myRoles/content-roles.html",
                                context_instance=RC(request))   
    else:
        return HttpResponseRedirect("/") 
     


def myHistoric(request):
    """Show the progress in the application"""
    if request.user.is_authenticated():
        user = request.user.username
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        return render_to_response("myHistoric/content-historic.html", 
                                    {'projects': projects},
                                    context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")


#__________________________ FILES _______________________________________#

'''
def progressBar(request):
    if request.method == 'POST':
        return render_to_response("prueba.html")
    else:
        return HttpResponseRedirect('/')

def upload_progress(request):
        """
        A view to report back on upload progress.
        Return JSON object with information about the progress of an upload.
        """
        print "LA PETICIÓN ES: \n" + str(request) + "\n"
        #import ipdb
        #ipdb.set_trace()
        progress_id = ''
        if 'X-Progress-ID' in request.GET:
            progress_id = request.GET['X-Progress-ID']
        elif 'X-Progress-ID' in request.META:
            progress_id = request.META['X-Progress-ID']
        if progress_id:
            cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
            data = cache.get(cache_key)
            return HttpResponse(simplejson.dumps(data))
        else:
            return HttpResponseServerError(
                'Server Error: You must provide X-Progress-ID header or query param.')
'''
#TO UNREGISTERED USER
def uploadUnregistered(request):
    """Upload file from form POST for unregistered users"""
    if request.method == 'POST':
        # Create BS of files
        file = request.FILES['zipFile']
        fileName = File (filename = file.name.encode('utf-8'))
        fileName.save()
        dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
        fileSaved = dir_zips + str(fileName.id) + ".sb2"
        print "FICHERO GUARDADO EN: " + fileSaved
        pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
        logFile = open (pathLog + "logFile.txt", "a")
        logFile.write("FileName: " + str(fileName.filename) + "\t" + "ID: " + \
        str(fileName.id) + "\n")
        # Save file in server
        counter = 0
        file_name = handle_uploaded_file(file, fileSaved, counter)
        # Analyze the scratch project
        d = analyzeProject(file_name)
        # Redirect to dashboard for unregistered user
        return render_to_response("upload/dashboard-unregistered.html", d)
    else:
        return HttpResponseRedirect('/')



def handle_uploaded_file(file, fileSaved, counter):
    # If file exists,it will save it with new name: name(x)
    if os.path.exists(fileSaved):
        counter = counter + 1
        if counter == 1:
            fileSaved = fileSaved.split(".")[0] + "(1).sb2"
        else:
            fileSaved = fileSaved.split('(')[0] + "(" + str(counter) + ").sb2"
        

        fileName = handle_uploaded_file(file, fileSaved, counter)
        return fileName
    else:
        with open(fileSaved, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return fileSaved



#_______________________URL Analysis Project_________________________________#

def processFormURL(request):
	"""Process Request of form URL"""
	if request.user.is_authenticated():
		user = request.user.username
	else:
		user = None
	if request.method == "POST":
		form = UrlForm(request.POST)
		if form.is_valid():
			d = {}
			flagsPlugin = {"Mastery":0, "DeadCode":0, "SpriteNaming":1, "Initialization":0, "DuplicateScripts":0}
			url = form.cleaned_data['urlProject']
			idProjectScratch = processStringUrl(url)
			if idProjectScratch == 'error':
				return HttpResponse('la url es incorrecta')
			else:
				fileName = sendRequestgetSB2(idProjectScratch)
				pathProject = '/home/test/github-des-titua/drScratch/drScratch/repo/' + fileName
				dicMetrics = analyzeProject(pathProject)
				if user == None:
					#updateDataBaseProject(idProjectScratch, dicMetrics)
					group = None
					dPlugins = buildDictPlugins2(flagsPlugin, 1, pathProject)
					d = buildDictResponse(dPlugins, int(idProjectScratch), group)
					buildJsonResponse(d)
					# Redirect to dashboard for unregistered user
					return render_to_response("upload/dashboard-unregistered.html", dicMetrics)
				else:
					updateProjectAuthUser(user, idProjectScratch, dicMetrics)
					# authenticated user
					return render_to_response("myprojects/content-projects.html", dicMetrics)

def buildDictPlugins(flags, allFlag, pathProject):
	"""Build dict with plugins in function flags"""
	ldict = []
	d = {}
	cond = allFlag
	allFlag = 0
	for key, value in flags.items():
		if (value or cond):
			print key + ' = ' + str(value)
			if ((key == "Mastery") or allFlag):
				dPlugin = pluginMasteryJson(pathProject)
			elif ((key == "DeadCode") or allFlag):
				dPlugin = pluginDeadCodeJson(pathProject)
			elif ((key == "SpriteNaming") or allFlag):
				dPlugin = pluginSpriteNamingJson(pathProject)
			elif ((key == "Initialization") or allFlag):
				dPlugin = pluginInitializationJson(pathProject)
			elif ((key == "DuplicateScripts") or allFlag):
				dPlugin = pluginDuplicateJson(pathProject)
			ldict.append(dPlugin.copy())
	d["plugins"] = ldict
	return d

def buildDictPlugins2(flags, allFlag, pathProject):
	"""Build dict with plugins in function flags"""
	dic = {}
	d = {}
	cond = allFlag
	allFlag = 0
	for key, value in flags.items():
		if (value or cond):
			if ((key == "Mastery") or allFlag):
				d.update(pluginMasteryJson(pathProject))
			elif ((key == "DeadCode") or allFlag):
				d.update(pluginDeadCodeJson(pathProject))
			elif ((key == "SpriteNaming") or allFlag):
				d.update(pluginSpriteNamingJson(pathProject))
			elif ((key == "Initialization") or allFlag):
				d.update(pluginInitializationJson(pathProject))
			elif ((key == "DuplicateScripts") or allFlag):
				d.update(pluginDuplicateJson(pathProject))
	dic["plugins"] = d
	return dic

def buildDictResponse(dPlugins, idProject, group):
	"""Build response Json"""
	d = {}
	date = str(datetime.now())
	dMastery = dPlugins["plugins"]["Mastery"]
	points = dMastery["points"]
	level = dMastery["level"]
	dinfo = {"version":1.0, "url":"drscratch.programamos.es"}	
	dproject = {"idProject":idProject, "group":group, "date":date, "points":points, "level":level}
	d["info"] = dinfo
	d["project"] = dproject
	d.update(dPlugins)
	return d

def buildJsonResponse(dic):
	json_data = json.dumps(dic)
	return json_data
				
def processStringUrl(url):
	"""Process String of URL from Form"""
	idProject = ''
	auxString = url.split("/")[-1]
	if auxString == '':
		# we need to get the other argument	
		possibleId = url.split("/")[-2]
		if possibleId == '#editor':
			idProject = url.split("/")[-3]
		else:
			idProject = possibleId
	else:
		if auxString == '#editor':
			idProject = url.split("/")[-2]
		else:
			# To get the id project
			idProject = auxString
	try:
		checkInt = int(idProject)
	except ValueError:
		idProject = 'error'
	return idProject

def sendRequestgetSB2(idProject):
	"""First request to getSB2"""
	getRequestSb2 = "http://getsb2.herokuapp.com/" + idProject
	nameFile = idProject + '.sb2'
	outputFile = 'repo/' + nameFile
	sb2File = urllib2.urlopen(getRequestSb2)
	output = open(outputFile, 'wb')
	output.write(sb2File.read())
	output.close()
	return nameFile


#_________________________ API  ___________________________#

def apiProject(request, idProject):
	"""Return json with metrics for project"""
	flagsPlugin = {"Mastery":0, "DeadCode":0, "SpriteNaming":0, "Initialization":0, "DuplicateScripts":0}
	fileName = sendRequestgetSB2(idProject)
	pathProject = '/home/test/github-des-titua/drScratch/drScratch/repo/' + fileName
	dPlugins = buildDictPlugins2(flagsPlugin, 1, pathProject)
	group = "Miclase"
	d = buildDictResponse(dPlugins, int(idProject), group)
	jsonMetrics = buildJsonResponse(d)
	print jsonMetrics
	return HttpResponse(jsonMetrics, content_type='application/json')
"""
def ajaxDogs(request):
	d = {"Mastery":{"flowcontrol":1, "logic":2}, "DeadCode":{"blocks":32}}
	jresponse = json.dumps(d)
    # convert the list to JSON
    return HttpResponse(jresponse, mimetype='application/json')
"""
def apiSetProject(request, teacher, group):
	"""Return set of projects in function group"""
	


#________________________JSON Response_______________________________________#


def responseMetricsJSON(request):
	"""Return the response in JSON format"""
	dic = pluginInitializationJson(fname)
	return 'hola'


def responseJson(request):
	"""Return the Json"""
	data = {'baz': 'goo', 'foo': 'bar'}
	json_data = json.dumps(data)

def pluginMasteryJson(fname):
	"""Return dic with Mastery plugin"""
	result = pluginResult(pMastery, fname)
	d = procMastery(result)
	return d

def pluginInitializationJson(fname):
	"""Return dict with plugin Initialization"""
	result = pluginResult(pInitialization, fname)
	d = procInitialization(result)
	return d

def pluginSpriteNamingJson(fname):
	"""Return dict with SpriteNaming plugin"""
	result = pluginResult(pSpriteNaming, fname)
	d = procSpriteNaming(result)
	return d

def pluginDeadCodeJson(fname):
	"""Return dict with DeadCode plugin"""
	result = pluginResult(pDeadCode, fname)
	d = procDeadCode(result)
	return d

def pluginDuplicateJson(fname):
	"""Return dict with Duplicate Scripts"""
	result = pluginResult(pDuplicateScript, fname)
	d = procDuplicateScript(result)
	return d

def pluginResult(plugin, fname):
	try:
		callHairball = plugin + fname
		result = os.popen(callHairball).read()
		return result
	except:
		print "IO Exception: execute os popen"	
		return "Error"


#_________________________STATITICS GRAPHS__________________________________#

def showStatisticsDr(request):
	"""Show the statics of projects"""
	allProjects = AnonProject.objects.all()

	#AnonProject.objects.filter(date__year=2015)
	begin_projects = AnonProject.objects.filter(level='beginner')
	dev_projects = AnonProject.objects.filter(level='developing')
	adv_projects = AnonProject.objects.filter(level='advanced')
	return render_to_response("statistics/content-statistics.html", 
                                {'projects': allProjects,
								'beginner': begin_projects,
								'developer': dev_projects,
								'advanced': adv_projects})

def getQueryAllProjects():
	"""Get a query for all analyzed projects"""
	allProjects = AnonProject.objects.all()	

def updateDataBaseProject(idProject, dicMetrics):
	"""Update in Data Base the metrics of project for anonymous"""
	dateUpdate = datetime.now()
	# Save the project
	aProject = AnonProject(identifier=int(idProject), date=dateUpdate, points=0, level="beginner")
	aProject.save()
	# Save the metrics    
	dmaster = dicMetrics["mastery"]
	aMastery = AnonMastery(myproject=aProject, abstraction=dmaster["Abstraction"], paralel=dmaster["Parallelization"], logic=dmaster["Logic"], synchronization=dmaster["Synchronization"], flowcontrol=dmaster["FlowControl"], interactivity=dmaster["UserInteractivity"], representation=dmaster["DataRepresentation"], scoring=dmaster["points"])
	aMastery.save()
	pointsProj = dmaster["points"]
	aProject.points = pointsProj
	aProject.level = levelProject(pointsProj)
	aProject.save()

def levelProject(points):
	"""Return the level of project in function of points"""
	level = ""
	if points > 15:	#CONST change
		level = "advanced"
	elif points > 7: #CONST change
		level = "developing"
	else:
		level = "beginner"
	return level


def updateProjectAuthUser(user, idProject, dictMetrics):
	"""Update the project in the data of user"""
	fupdate = datetime.now()
	# Get the dashboard of user
	myDashboard = Dashboard.objects.get(user=user)    
	# Save the project
	newProject = Project(name='AnalyzedByUrl', version=1, points=0, path='AnalyzedByUrl', fupdate=fupdate, dashboard=myDashboard)
	newProject.save()
	# Save the metrics    
	dmaster = dictMetrics["mastery"]
	newMastery = Mastery(myproject=newProject, abstraction=dmaster["Abstraction"], paralel=dmaster["Parallelization"], logic=dmaster["Logic"], synchronization=dmaster["Synchronization"], flowcontrol=dmaster["FlowControl"], interactivity=dmaster["UserInteractivity"], representation=dmaster["DataRepresentation"], points=dmaster["points"])
	newMastery.save()
	newProject.points = dmaster["points"]
	newProject.level = levelProject(dmaster["points"])    
	newProject.save()      
	for charx, dmetric in dictMetrics["attribute"].items():
		if charx != 'stage':
			newAttribute = Attribute(myproject=newProject, character=charx, orientation=dmetric["orientation"], position=dmetric["position"], costume=dmetric["costume"], visibility=dmetric["visibility"], size=dmetric["size"])
			newAttribute.save()
	iterator = 0
	for deadx in dictMetrics["dead"]:
		if (iterator % 2) == 0:
			newDead = Dead(myproject=newProject, character=deadx, blocks=0)
		else:
			newDead.blocks = deadx
		newDead.save()
		iterator += 1

	newDuplicate = Duplicate(myproject=newProject, numduplicates=dictMetrics["duplicate"][0])
	newDuplicate.save()
	for charx in d["sprite"]:
		newSprite = Sprite(myproject=newProject, character=charx)
		newSprite.save()


#_______________________ AUTOMATIC ANALYSIS _________________________________#

def analyzeProject(file_name):
    dictionary = {}
    if os.path.exists(file_name):
		#Request to hairball
		metricMastery = "hairball -p mastery.Mastery " + file_name
		metricDuplicateScript = "hairball -p \
				                duplicate.DuplicateScripts " + file_name
		metricSpriteNaming = "hairball -p convention.SpriteNaming " + file_name
		metricDeadCode = "hairball -p blocks.DeadCode " + file_name 
		metricInitialization = "hairball -p \
				           initialization.AttributeInitialization " + file_name

		#Plug-ins not used yet
		#metricBroadcastReceive = "hairball -p 
		#                          checks.BroadcastReceive " + file_name
		#metricBlockCounts = "hairball -p blocks.BlockCounts " + file_name
		#Response from hairball
		resultMastery = os.popen(metricMastery).read()
		resultDuplicateScript = os.popen(metricDuplicateScript).read()
		resultSpriteNaming = os.popen(metricSpriteNaming).read()
		resultDeadCode = os.popen(metricDeadCode).read()
		resultInitialization = os.popen(metricInitialization).read()
		#Plug-ins not used yet
		#resultBlockCounts = os.popen(metricBlockCounts).read()
		#resultBroadcastReceive = os.popen(metricBroadcastReceive).read()

		#Create a dictionary with necessary information
		dictionary.update(procMastery(resultMastery))
		dictionary.update(procDuplicateScript(resultDuplicateScript))
		dictionary.update(procSpriteNaming(resultSpriteNaming))
		dictionary.update(procDeadCode(resultDeadCode))
		dictionary.update(procInitialization(resultInitialization))
		#Plug-ins not used yet
		#dictionary.update(procBroadcastReceive(resultBroadcastReceive))
		#dictionary.update(procBlockCounts(resultBlockCounts))
		return dictionary
    else:
        return HttpResponseRedirect('/')


# __________________________ PROCESSORS _____________________________#

def procMastery(lines):
	"""Processor plugin Mastery"""
	dic = {}
	lLines = lines.split('\n')
	d = ast.literal_eval(lLines[1])
	level = lLines[4].split(':')[1]
	lLines = lLines[2].split(':')[1]
	points = int(lLines.split('/')[0])
	maxPoints = int(lLines.split('/')[1])
	d["points"] = points
	d["maxPoints"] = maxPoints
	d["level"] = level
	dic["Mastery"] = d
	return dic

def procDuplicateScript(lines):
	"""Return number of duplicate scripts"""
	dic = {}
	d = {}
	dFinal = {}
	sec = []
	total = 0
	i = 0
	blocks = []
	lLines = lines.split('\n')
	if len(lLines) > 2:
		total = lLines[1][0]
		blocks = lLines[2:]
		blocks = blocks[:-2]
		dic["total"] = total
		for block in blocks:
			idDic = "strBlock" + str(i)
			sec.append(idDic)
			i += 1
		d = dict(zip(sec, blocks))
		dic["blocks"] = d
		dFinal["DuplicateScripts"] = dic
	else:
		# no duplicate scripts
		dic["total"] = total #0
		dic["blocks"] = d  #{}
		dFinal["DuplicateScripts"] = dic
	return dFinal
		
def procSpriteNaming(lines):
	"""Return the number of default spring"""
	dic = {}
	d = {}
	dFinal = {}
	i = 0
	sec = []
	lLines = lines.split('\n')
	if len(lLines) > 2:
		number = lLines[1].split(' ')[0]
		charts = lLines[2:]
		charts = charts[:-1]
		dic["total"] = str(number)
		for c in charts:
			idDic = "character" + str(i)
			sec.append(idDic)
			i += 1
		d = dict(zip(sec, charts))
		dic["characters"] = d
	else:
		# no SpriteNaming
		dic["total"] = 0
		dic["characters"] = d
	dFinal["SpriteNaming"] = dic
	return dFinal


def procDeadCode(lines):
	"""Number of dead code with characters and blocks"""
	lLines = lines.split('\n')
	lLines = lLines[1:]
	iterator = 0
	dItem = {}
	dic = {}
	dFinal = {}
	lItems = []
	for frame in lLines:
		if '[kurt.Script' in frame:
			# Found an object
			name = frame.split("'")[1]
			#lcharacter.append(name)
			dItem["character"] = name
		if 'kurt.Block' in frame:
		    iterator += 1
		if 'pos=' in frame:
			dItem["blocks"] = iterator
			iterator = 0
			aux = frame.split('=')[1]
			dItem["posx"] = (aux.split(',')[0]).split('(')[1]
			dItem["posy"] = (aux.split(',')[1]).split(')')[0]
			lItems.append(dItem.copy())
	dic["total"] = len(lItems)
	dic["deadBlocks"] = lItems
	dFinal["DeadCode"] = dic
	return dFinal

def procInitialization(lines):
	"""Processor Initialization plugin"""
	dic = {}
	lLines = lines.split('.sb2')
	d = ast.literal_eval(lLines[1])
	dFinal = {}
	keys = d.keys()
	values = d.values()
	items = d.items()
	number = 0
	for keys, values in items:
		list = []
		attribute = ""
		internalkeys = values.keys()
		internalvalues = values.values()
		internalitems = values.items()
		flag = False
		counterFlag = False
		i = 0
		for internalkeys, internalvalues in internalitems:
		    if internalvalues == 1:
		        counterFlag = True
		        for value in list:
		            if internalvalues == value:
		                flag = True
		        if not flag:
		            list.append(internalkeys)
		            if len(list) < 2:
		                attribute = str(internalkeys)
		            else:
		                attribute = attribute + ", " + str(internalkeys)
		if counterFlag:
		    number = number + 1
		d[keys] = attribute
	
	for k, v in d.items():
		if v == '':
			# delete key from dict
			del(d[k])
	dic["total"] = number
	dic["characters"] = d
	dFinal["Initialization"] = d
	return dFinal

# ___________________ PROCESSORS OF PLUG-INS NOT USED YET ___________________#

#def procBlockCounts(lines):
#    """CountLines"""
#    dic = {}
#    dic["countLines"] = lines

#    print "BLOCK COUNTS: " + str(dic)
#    return dic


#def procBroadcastReceive(lines):
#    """Return the number of lost messages"""
#    dic = {}
#    lLines = lines.split('\n')
    # messages never received or broadcast
#    laux = lLines[1]
#    laux = laux.split(':')[0]
#    dic["neverRB"] = dic
#    dic["neverRB"]["neverReceive"] = laux
#    laux = lLines[3]
#    laux = laux.split(':')[0]
#    dic["neverRB"]["neverBroadcast"] = laux
    
#    return dic

#___________________________ UNDER DEVELOPMENT _________________________#

#UNDER DEVELOPMENT: Children!!!Carefull
def registration(request):
    """Registration a user in the app"""
    return render_to_response("formulary.html")


#UNDER DEVELOPMENT: Children!!!Carefull
def profileSettings(request):
    """Main page for registered user"""
    return render_to_response("profile.html")

#UNDER DEVELOPMENT:
#TO REGISTERED USER
def uploadRegistered(request):
    """Upload and save the zip"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        return HttpResponseRedirect('/')
        
    if request.method == 'POST':
        form = UploadFileForm(request.POST)
        # Analyze the scratch project and save in our server files
        fileName = handle_uploaded_file(request.FILES['zipFile'])
        # Analize project and to save in database the metrics
        d = analyzeProject(fileName)
        fupdate = datetime.now()
        # Get the short name
        shortName = fileName.split('/')[-1]
        # Get the dashboard of user
        myDashboard = Dashboard.objects.get(user=user)    
        # Save the project
        newProject = Project(name=shortName, version=1, score=0, path=fileName, fupdate=fupdate, dashboard=myDashboard)
        newProject.save()
        # Save the metrics    
        dmaster = d["mastery"]
        newMastery = Mastery(myproject=newProject, abstraction=dmaster["Abstraction"], paralel=dmaster["Parallelization"], logic=dmaster["Logic"], synchronization=dmaster["Synchronization"], flowcontrol=dmaster["FlowControl"], interactivity=dmaster["UserInteractivity"], representation=dmaster["DataRepresentation"], TotalPoints=dmaster["TotalPoints"])
        newMastery.save()
        newProject.score = dmaster["Total{% if forloop.counter0|divisibleby:1 %}<tr>{% endif %}Points"]
        print "Puntos:" 
        print newProject.score
        if newProject.score > 15:
            newProject.level = "advanced"
        elif newProject.score > 7:
            newProject.level = "developing"
        else:
            newProject.level = "beginner"
        newProject.save()
        
        for charx, dmetrics in d["attribute"].items():
            if charx != 'stage':
                newAttribute = Attribute(myproject=newProject, character=charx, orientation=dmetrics["orientation"], position=dmetrics["position"], costume=dmetrics["costume"], visibility=dmetrics["visibility"], size=dmetrics["size"])
            newAttribute.save()

        iterator = 0
        for deadx in d["dead"]:
            if (iterator % 2) == 0:
                newDead = Dead(myproject=newProject, character=deadx, blocks=0)
            else:
                newDead.blocks = deadx
            newDead.save()
            iterator += 1
        
        newDuplicate = Duplicate(myproject=newProject, numduplicates=d["duplicate"][0])
        newDuplicate.save()
        for charx in d["sprite"]:
            newSprite = Sprite(myproject=newProject, character=charx)
            newSprite.save()
            print newSprite.character
        return HttpResponseRedirect('/myprojects')

#_____ ID/BUILDERS ____________#

def idProject(request, idProject):
    """Resource uniquemastery of project"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = None
    dmastery = {}
    project = Project.objects.get(id=idProject)
    item = Mastery.objects.get(myproject=project)
    dmastery = buildMastery(item)
    TotalPoints = dmastery["TotalPoints"]
    dsprite = Sprite.objects.filter(myproject=project)
    ddead = Dead.objects.filter(myproject=project)
    dattribute = Attribute.objects.filter(myproject=project)
    listAttribute = buildAttribute(dattribute)
    numduplicate = Duplicate.objects.filter(myproject=project)[0].numduplicates
    return render_to_response("project.html", {'project': project,
                                                'dmastery': dmastery,
                                                'lattribute': listAttribute,
                                                'numduplicate': numduplicate,
                                                'dsprite': dsprite,
                                                'Total points': TotalPoints,
                                                'ddead': ddead},
                                                context_instance=RequestContext(request))
    



def buildMastery(item):
    """Generate the dictionary with mastery"""
    dmastery = {}
    dmastery["Total points"] = item.TotalPoints
    dmastery["Abstraction"] = item.abstraction
    dmastery["Parallelization"] = item.paralel
    dmastery["Logic"] = item.logic
    dmastery["Synchronization"] = item.synchronization
    dmastery["Flow Control"] = item.flowcontrol
    return dmastery

def buildAttribute(qattribute):
    """Generate dictionary with attribute"""
    # Build the dictionary
    dic = {}
    for item in qattribute:
        dic[item.character] = {"orientation": item.orientation, 
                                "position": item.position, 
                                "costume": item.costume, 
                                "visibility":item.visibility, 
                                "size": item.size}
    listInfo = writeErrorAttribute(dic)
    return listInfo

#_______BUILDERS'S HELPERS ________#

def writeErrorAttribute(dic):
    """Write in a list the form correct of attribute plugin"""
    lErrors = []
    for key in dic.keys():
        text = ''
        dx = dic[key]
        if key != 'stage':
            if dx["orientation"] == 1:
                text = 'orientation,'
            if dx["position"] == 1:
                text += ' position, '
            if dx["visibility"] == 1:
                text += ' visibility,'
            if dx["costume"] == 1:
                text += 'costume,'
            if dx["size"] == 1:
                text += ' size'
            if text != '':
                text = key + ': ' + text + ' modified but not initialized correctly'
                lErrors.append(text)
            text = None
        else:
            if dx["background"] == 1:
                text = key + ' background modified but not initialized correctly'
                lErrors.append(text)
    return lErrors



# _________________________  _______________________________ #

def uncompress_zip(zip_file):
    unziped = ZipFile(zip_file, 'r')
    for file_path in unziped.namelist():
        if file_path == 'project.json':
            file_content = unziped.read(file_path)
    show_file(file_content)

