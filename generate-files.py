import argparse
import click
import shutil
import os
import sys

DEBUG_OUTPUT = False

# global vars for project setup
project=""
service=""
stage=""
sequence=""
tasks=[]
# global file paths
shipyardFile=""
dynatraceConfigurationFile=""
sequenceTriggerEventFile=""

# https://keptn.sh/docs/0.12.x/manage/shipyard/#reserved-keptn-tasks
reservedTasks=["evaluation"]

def debugMessage(message):
    if DEBUG_OUTPUT:
        print(message)

def createFiles():

    # generated folder is the name of the project
    projectpath=os.path.join("gen",project)

    # remove if it exists and then create the project folder
    debugMessage("DEBUG - createFiles(): deleting " + projectpath)
    shutil.rmtree(projectpath)
    os.makedirs(projectpath, exist_ok=True)
    
    # now make the project files
    genShipyard(projectpath)
    genDynatraceConfig(projectpath)
    genSequenceTriggerEvent(projectpath)
    # make finished events except for reserved words
    for x in range(len(tasks)):
        if (tasks[x] in reservedTasks):
            debugMessage("DEBUG - createFiles(): Skipping reserved task: "+tasks[x])
            continue
        else:
            genTaskFinishedEvent(projectpath,tasks[x])

def genShipyard(projectpath):

    # make global because use in displayScriptCommand()
    global shipyardFile

    fileBody= 'apiVersion: spec.keptn.sh/0.2.2\n' 
    fileBody+='kind: "Shipyard"\n'
    fileBody+='metadata:\n'
    fileBody+='  name: "Generated for '+ project+ '"\n'
    fileBody+='spec:\n'
    fileBody+='  stages:\n'
    fileBody+='    - name: "'+ stage+ '"\n'
    fileBody+='      sequences:\n'
    fileBody+='      - name: "' + sequence + '"\n'
    fileBody+='        tasks:\n'

    # add a defaults of the required properties for evaluation tasks
    for x in range(len(tasks)):
        fileBody+='        - name: "'+tasks[x]+'"\n'
        if (tasks[x] == "evaluation"):
            fileBody+='          properties:\n'
            fileBody+='            timeframe: "5m"\n'

    shipyardFile=os.path.join(projectpath, "shipyard.yaml")
    makeFileFromString(shipyardFile,fileBody)

def genSequenceTriggerEvent(projectpath):

    # make global because use in displayScriptCommand()
    global sequenceTriggerEventFile

    fileBody= '{\n'
    fileBody+='  "data": {\n'
    fileBody+='    "project":"'+project+'",\n'
    fileBody+='    "stage":"'+stage+'",\n'
    fileBody+='    "service": "'+service+'"\n'
    fileBody+='  },\n'
    fileBody+='  "source": "keptn-project-gen",\n'
    fileBody+='  "specversion": "1.0",\n'
    fileBody+='  "type": "sh.keptn.event.'+stage+'.'+sequence+'.triggered"\n'
    fileBody+='}\n'

    eventFileName=stage+'.'+sequence+".triggered.json"
    sequenceTriggerEventFile=os.path.join(projectpath, eventFileName)
    makeFileFromString(sequenceTriggerEventFile,fileBody)

def genTaskFinishedEvent(projectpath,task):

    fileBody= '{\n'
    fileBody+='  "data": {\n'
    fileBody+='    "project":"'+project+'",\n'
    fileBody+='    "stage":"'+stage+'",\n'
    fileBody+='    "service": "'+service+'",\n'
    fileBody+='    "status": "succeeded",\n'
    fileBody+='    "result": "pass"\n'
    fileBody+='  },\n'
    fileBody+='  "source": "keptn-project-gen",\n'
    fileBody+='  "specversion": "1.0",\n'
    fileBody+='  "type": "sh.keptn.event.'+task+'.finished",\n'
    fileBody+='  "shkeptncontext": "REPLACE_ID",\n'
    fileBody+='  "triggeredid": "REPLACE_TRIGGER_ID"\n'
    fileBody+='}\n'

    eventFileName=task+".finished.json"
    taskFinishedEventFile=os.path.join(projectpath, eventFileName)
    makeFileFromString(taskFinishedEventFile,fileBody)

def genDynatraceConfig(projectpath):
    # https://github.com/keptn-contrib/dynatrace-service/blob/master/documentation/dynatrace-conf-yaml-file.md

    # make global because use in displayScriptCommand()
    global dynatraceConfigurationFile

    fileBody= "spec_version: '0.1.0'\n"
    fileBody+='dashboard: query\n'
    fileBody+='attachRules:\n'
    fileBody+='  tagRule:\n'
    fileBody+='  - meTypes:\n'
    fileBody+='    - SERVICE\n'
    fileBody+='    tags:\n'
    fileBody+='    - context: CONTEXTLESS\n'
    fileBody+='      key: keptn_project\n'
    fileBody+='      value: $PROJECT\n'
    fileBody+='    - context: CONTEXTLESS\n'
    fileBody+='      key: keptn_service\n'
    fileBody+='      value: $SERVICE\n'
    fileBody+='    - context: CONTEXTLESS\n'
    fileBody+='      key: keptn_stage\n'
    fileBody+='      value: $STAGE\n'

    dynatraceConfigurationFile=os.path.join(projectpath, "dynatrace.conf.yaml")
    makeFileFromString(dynatraceConfigurationFile,fileBody)

def makeFileFromString(projectpath,thestring):
    debugMessage("DEBUG - makeFileFromString(): " + projectpath)

    text_file = open(projectpath, "w")
    text_file.write(thestring)

def printVariables():
    print("")
    print("==============================================================================")
    print("  Project         : " + project)
    print("  Service         : " + service)
    print("  Stage           : " + stage)
    print("  Sequence        : " + stage)
    print("  Sequence Tasks  : " + ' '.join(tasks)) 
    print("==============================================================================")

def gatherInputs():
    global project
    global service
    global stage
    global sequence
    global tasks
    project=click.prompt("Enter project name     ", type=str) # default=""
    service=click.pr3ompt("Enter service name     ", type=str)
    stage=click.prompt("Enter stage name       ", type=str)
    sequence=click.prompt("Enter sequence name    ", type=str)
    # limit to 5 tasks for if blank entered than exit
    i = 0
    print("You will now be prompted in a loop for '" + sequence + "' sequence tasks names")
    print("Enter 'q' to exit loop")
    while i < 6:
        thetask=click.prompt("Enter task #    " + str(i+1) + " name ", type=str)
        if (thetask == "q") and (i > 0):
            break
        tasks.append(thetask)
        i += 1

def validateInputs():
    if (project == "") or (project is None): sys.exit("ABORT: Missing value for project")
    if (service == "") or (service is None): sys.exit("ABORT: Missing value for service")
    if (stage == "") or (stage is None): sys.exit("ABORT: Missing value for stage")
    if (sequence == "") or (sequence is None): sys.exit("ABORT: Missing value for sequence")
    if len(tasks) < 1: sys.exit("ABORT: Missing value for sequence task 1")

def displayScriptCommand():
    print("")
    print("Run this script to onboard your project")
    print("python create-project.py \\")
    print("  --project " + project + " \\")
    print("  --service " + service + " \\")
    print("  --stage " + stage + " \\")
    print("  --shipyard " + shipyardFile + " \\")
    print("  --dtconf " + dynatraceConfigurationFile)
    print("")
    print("Run this command to trigger your sequence")
    print("keptn send event --file "+sequenceTriggerEventFile)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--debug', help='Enable debug output', action='store_true')
    ap.add_argument("--project", help="Project name")
    ap.add_argument("--service", help="Service name")
    ap.add_argument("--stage", help="Stage name")
    ap.add_argument("--sequence", help="Sequence name")
    ap.add_argument("--task1", help="Sequence Task 1 name")
    ap.add_argument("--task2", help="Sequence Task 2 name")
    ap.add_argument("--task3", help="Sequence Task 3 name")
    ap.add_argument("--task4", help="Sequence Task 4 name")
    ap.add_argument("--task5", help="Sequence Task 5 name")

    args = vars(ap.parse_args())
    if args["debug"]:
        DEBUG_OUTPUT = True

    # if pass in project argument, then assume the others will be
    # if not passed then prompt for them
    if args["project"] is not None:
        project = args["project"]
        service = args["service"]
        stage = args["stage"]
        sequence = args["sequence"]
        if args["task1"] is not None: tasks.append(args["task1"])
        if args["task2"] is not None: tasks.append(args["task2"])
        if args["task3"] is not None: tasks.append(args["task3"])
        if args["task4"] is not None: tasks.append(args["task4"])
        if args["task5"] is not None: tasks.append(args["task5"])
    else:
        gatherInputs()

    validateInputs()
    printVariables()
    createFiles()
    displayScriptCommand()
