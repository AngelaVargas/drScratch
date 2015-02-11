#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Drawer():
	version = 1.0

	def drawBlockfromScript(script):
		"""From string return the content for scratchblocks2"""
		sentences = script.split(",")
		sentences[0] = sentences[0].split('[')[1]
		sentences[-1] = sentences[-1].split(']')[0]		
		for inst in sentences:
			if '%s' in inst:
				inst.replace("%s", "(%s)")
	
