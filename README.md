# Overview

This is a helper script to generate project files to help in testing and demos. By providing the common inputs of project, service, stage, sequence and task names, this utility will generate a shipyard and example events files. 

This script is limited to one stage, one sequence and 5 sequence tasks.  


# Generate project files

After running the `generate-files.py` python script, a set of files will be added to a `gen/project` subfolder.  

NOTE: If you run or re-run this script, the project `gen/project` subfolder will be deleted and recreated.

## Prerequistes

1. Python3 and Pip installed locally
1. Clone repo
1. Run `pip install --no-cache-dir -r requirements.txt`

## Usage 

There are two options for using this script:s

### Option 1: Run script with a prompt for values

Run this command:

```
python generate-files.py
```

Example prompts:

```
Enter project name     : jira-demo
Enter service name     : tnt-demo-svc 
Enter stage name       : production
Enter sequence name    : problem-notification
You will now be prompted in a loop for 'problem-notification' sequence tasks names
Enter 'q' to exit loop
Enter task #    1 name : create-jira
Enter task #    2 name : evaluation
Enter task #    3 name : update-jira
Enter task #    4 name : q
```

### Option 2: Run script with command line arguments

Edit the below for your needs. Up to 5 task arguments are supported.

```
python generate-files.py \
    --project jira-demo \
    --service tnt-demo-svc \
    --stage production \
    --sequence problem-notification \
    --task1 create-jira \
    --task2 evaluation \
    --task3 update-jira
```

# Use project files

The `generate-files.py` script generates files put into the `gen/project` subfolder and it shows some command you can cut-n-paste as shown in the example below:

    ```
    Run this script to onboard your project
    python create-project.py \
        --project jira-demo \
        --service tnt-demo-svc \
        --stage production \
        --shipyard gen/jira-demo/shipyard.yaml \
        --dtconf gen/jira-demo/dynatrace.conf.yaml

    Run this command to trigger your sequence
    keptn send event --file gen/jira-demo/production.problem-notification.triggered.json
    ```

The `create-project.py` will automate the calls using these keptn CLI commands:
* `keptn create project`
* `keptn create service`
* `keptn add-resource` for the Dynatrace configuration files

## Prerequistes

1. If using the `create-project.py` script, it assumes the keptn CLI is installed and authenticated with the `keptn auth` command.
1. Ensure that your service is monitored by Dynatrace with the corrects tags and has a SLO dashboard
1. Ensure that your Keptn environment has a `dynatrace` secret and API required by the [Dynatrace integration](https://keptn.sh/docs/0.12.x/monitoring/dynatrace/install/#install-dynatrace-keptn-integration)

## Usage

1. Before you run `create-project.py`, review and adjust the generated files for your needs.
    * For example the [dynatrace.conf.yaml](https://github.com/keptn-contrib/dynatrace-service/blob/master/documentation/dynatrace-conf-yaml-file.md#attach-rules-for-connecting-dynatrace-entities-with-events-attachrules) file.
1. Copy and paste the commands in the output from the `generate-files.py` script. 
1. Setup your project with an [upstream repo](https://keptn.sh/docs/0.12.x/manage/git_upstream/).  Below is Keptn CLI example:
    ```
    keptn update project jira-demo \
        --git-remote-url=https://github.com/[MY ORG]/[MY REPO].git \
        --git-user=[MY USERNAME] \
        --git-token=[MY TOKEN]
    ```
1. Review the Bridge Web UI to validate project onboarding and sequence execution
