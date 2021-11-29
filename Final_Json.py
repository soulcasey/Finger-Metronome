import json
from os.path import exists

filename = "savefile.json" #Initialize file name

def load(): #Load or create a Json files
    tempo = {}
    if exists(filename): #Check if Json file exists already
	    file = open(filename,'r') #Open the Json file if it does exist already
	    tempoText = file.read()
	    tempo = json.loads(tempoText) #Receive the already writen Json file
    else:
	    tempo["Tempo"] = 45
	    tempo_json = json.dumps(tempo)
	    file = open(filename, "w") #Create a new Json file if it doesn't exist already
	    file.write(tempo_json) 
	    file.close()
    return tempo["Tempo"]

newTempo = {}
def save(value): #Save the tempo values to the Json file
	newTempo["Tempo"] = value
	tempo_json = json.dumps(newTempo)
	file = open(filename, "w") #Overwrite the already existing values
	file.write(tempo_json)
	file.close()