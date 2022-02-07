import os
import subprocess
import argparse

def executeCommand(cmd, opts):
  args=[]
  args.append(cmd)
  for i in opts.split():
      args.append(i)
  print('###############')
  print('executeCommand: ' + cmd + ' ' + opts)
  output = subprocess.run(args)

def validateKeptn():
  # Get Version
  cmd="keptn"
  opts="version"
  executeCommand(cmd,opts)

  # Get Status
  cmd="keptn"
  opts="status"
  executeCommand(cmd,opts)

def create_project():

  # Create project
  cmd="keptn"
  opts="create project " + project + " --shipyard=" + shipyard
  executeCommand(cmd,opts)

  # Create service within the project
  cmd="keptn"
  opts="create service " + service + " --project=" + project
  executeCommand(cmd,opts)

  # Validate that service was created
  if dtconf:
    cmd="keptn"
    opts="add-resource --project=" + project + " --resource=" + dtconf + " --resourceUri=dynatrace/dynatrace.conf.yaml"
    executeCommand(cmd,opts)
  else:  
    print("Skipping adding dynatrace.conf.yaml")

def printVariables():
    print("")
    print("==============================================================================")
    print("  Project           : " + project)
    print("  Service           : " + service)
    print("  Stage             : " + stage)
    print("  Shipyard filename : " + shipyard)
    print("  Dynatrace Conf    : " + dtconf) 
    print("==============================================================================")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--debug', help='Enable debug output', action='store_true')
    ap.add_argument("--project", required=True, help="Project name")
    ap.add_argument("--service", required=True, help="Service name")
    ap.add_argument("--stage", required=True, help="Stage name")
    ap.add_argument("--shipyard", required=True, help="Shipyard filename")
    ap.add_argument("--dtconf", help="Dynatrace Configuration filename")

    args = vars(ap.parse_args())
    if args["debug"]:
        DEBUG_OUTPUT = True

    project = args["project"]
    service = args["service"]
    stage = args["stage"]
    shipyard = args["shipyard"]
    dtconf = args["dtconf"]

    validateKeptn()
    printVariables()
    proceedInput = input ("Proceed? (y/n)")
    if (proceedInput == "y"):
      create_project()
