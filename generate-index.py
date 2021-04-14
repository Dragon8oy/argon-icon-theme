#!/usr/bin/python3
import sys, shutil, os, csv
from icon_builder import createContextDict

def generateIndex(buildDir):
  #Load info from index/context.csv into a dictionary
  contextDict = createContextDict(None)

  #Copy index/index.theme.template to buildDir/index.theme
  shutil.copy("index/index.theme.template", buildDir + "/index.theme")

  #Function to return array of all subdirectories of searchDir
  def getDirList(searchDir):
    dirList = []
    for dir in os.listdir(searchDir):
      if os.path.isdir(searchDir + "/" + dir):
        dirList.append(dir)
    return dirList

  #Create ordered array of resolution directories
  resolutionDirs=os.popen("echo " + ' '.join(getDirList(buildDir)) + '| tr " " "\n" | sort -V | tr "\n" " "').read().split()

  #Arrays / variables for next loop
  directoryAccumulator = []
  directoryInfo = []

  #Iterate through each resolution and begin processing
  for iconResolution in resolutionDirs:
    #Get, sort and iterate through each icon category
    iconDirs=getDirList(buildDir + "/" + iconResolution)
    for iconDir in sorted(iconDirs):
      #Check icon category has a matching entry in index/context.csv
      if iconDir in contextDict:
        #Generate values for index entry
        if iconResolution == "scalable":
          iconSize = 256
          iconType = "Scalable"
        else:
          iconSize = iconResolution.split('x')[0]
          iconType = "Fixed"

        #Keep running total of all dirs processed
        directoryAccumulator.append(iconResolution + "/" + iconDir)

        #Fill in directory.template and index.theme
        directoryInfo.append("")
        directoryInfo.append("[" + iconResolution + "/" + iconDir + "]")
        directoryInfo.append("Size=" + str(iconSize))
        directoryInfo.append("Context=" + contextDict[iconDir][0])
        directoryInfo.append("Type=" + iconType)

  #Prepare arrays to be written to file
  outputData = [""] + ["Directories=" + ",".join(directoryAccumulator)] + directoryInfo

  #Write outputData to buildDir/index.theme
  with open(buildDir + "/index.theme", 'a') as file:
    for line in outputData:
      file.write(line + "\n")

#Handle arguments
if sys.argv[1] == "--index":
  #Pass generateIndex() the build directory
  generateIndex(str(sys.argv[2]))
