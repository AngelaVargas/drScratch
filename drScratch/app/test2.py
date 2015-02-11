#!/usr/bin/env python
# -*- coding: utf-8 -*-
pMastery = "hairball -p mastery.Mastery "
pDuplicateScript = "hairball -p duplicate.DuplicateScripts " 
pSpriteNaming = "hairball -p convention.SpriteNaming "
pDeadCode = "hairball -p blocks.DeadCode "
pInitialization = "hairball -p initialization.AttributeInitialization "
pathProject = '/home/test/zipFiles/' + 'elsa.sb2'
				

def pluginResult(plugin, fname):
	try:
		callOs = plugin + fname
		result = os.popen(callOs).read()
		return result
	except:
		print "IO Exception: execute os popen"	
		return "Error"


def pluginInitializationJson(fname):
	"""Return a dictionary with the metrics of Initialization"""
	result = pluginResult(pInitialization, fname)
	# We need to check the failures of initialization
	d = procInitialization(result)
	return d

def pluginDeadCodeJson(fname):
	"""Return """
	result = pluginResult(pSpriteNaming, fname)
	# We need to check the failures of initialization
	d = procDeadCode(result)
	return d


def procDeadCode(lines):
	"""Number of dead code with characters and blocks"""
	lLines = lines.split('\n')
	lLines = lLines[1:]
	lcharacter = []
	literator = []
	lblocks = []
	iterator = 0
	dItem = {}
	listDItems = []
	scriptsCount = 0
	for frame in lLines:
		if '[kurt.Script' in frame:
			# Found an object
			name = frame.split("'")[1]
			if name == '':
				# script of character
				scriptsCount += 1
			else:
				# new character
				d["scripts"] = scriptsCount
				scriptsCount = 0
				lcharacter.append(name)
				dItem["character"] = name
				if iterator != 0:
					literator.append(iterator)		
					iterator = 0
		if 'kurt.Block' in frame:
		    iterator += 1
		if 'pos=' in frame:
			dItem["blocks"] = iterator
			aux = frame.split('=')[1]
			dItem["posx"] = (aux.split(',')[0]).split('(')[1]
			dItem["posy"] = (aux.split(',')[1]).split(')')[0]
		listDItems.append(dItem)
		dItem.clear()
	dItem["scripts"] = scriptsCount
	listDItems.append(dItem)
	print listDItems
	"""    literator.append(iterator)
	dItem["blocks"] = iterator

	number = len(lcharacter)
	dic = {}
	dic["total"] = number
	#for i in range(number):
	#    dic[lcharacter[i]] = literator[i]
	d = dict(zip(lcharacter, literator))
	dic['characters'] = d
	"""
	dic = {}
	return dic


def procInitialization(lines):
	"""Processor Initialization plugin"""
	dic = {}
	lLines = lines.split('.sb2')
	d = ast.literal_eval(lLines[1])
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
		
	dic["initialization"] = d
	dic["initialization"]["total"] = number
	return dic

def start():
	pluginResult(pDeadCode, pathProject)
	pluginResult(pInitialization, pathProject)

