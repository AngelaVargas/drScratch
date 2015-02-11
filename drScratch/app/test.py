
def uploadRegistered(request):
    """Upload and save the zip"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        return HttpResponseRedirect('/')
        
    if request.method == 'POST':
        form = UploadFileForm(request.POST)


        d = analyzeProject(fileName)
        fupdate = datetime.now()
        
		 # Save the project
        newProject = Project(identifier=idProject, date=fupdate, score=0, level="")
        newProject.save()
        # Save the metrics    
        dmaster = d["mastery"]
        newMastery = Mastery(myproject=newProject, abstraction=dmaster["Abstraction"], paralel=dmaster["Parallelization"], logic=dmaster["Logic"], synchronization=dmaster["Synchronization"], flowcontrol=dmaster["FlowControl"], interactivity=dmaster["UserInteractivity"], representation=dmaster["DataRepresentation"], points=dmaster["TotalPoints"])

		newMastery.save()

        
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

