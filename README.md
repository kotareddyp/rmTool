# RightMove Interview Solution

### Outline

Here is a solution for the interview question sent to me by the recruiter. This is written using python. I have attached the instructions file sent to me (PlatformsPrep)

## Requirements

Essentially, the requirement is to instantiate a container using an image that is already available on the current host.

## Tooling used

In strict adherence to the Prep document I have used docker. On my machine I have Python 3

## Prerequisites

Follow the PlatformPrep document and create images (conversation/hello and conversation/say-goodbye)
And, run docker compose to keep the mock API service running on your machine (detailed instructions are in the PlatformPrep document
Note: Do not issue docker compose down until you have tested this tool

## How to use this tool?

1. Download/clone the repo
2. In the home directory issue the following commands to initiate a python virtual environment
  ```
<!-- Crete a local virtual environment   -->
  python -m venv .venv
  source ./venv/Scripts/activate
  pip install -r requirements.txt
  ```
3. After completing the above steps, you are ready to run this tool
4. Issue the following command on terminal
  ```
  cd <to the directory where you downloaded this repo to (or cloned to)
  <!-- To run unit tests, use option -b to buffer stdout and stderr   -->
  python -m unittest unit_tests.py -b
  python main.py
  ```
5. Answer 'yes' to the prompt
6. If it worked, you will find the output in a file called output.log and the program will exit

Note: If you run the tool again (using python main.py), it will fail because the host port would have already bound from the previously created container, to run again you will have to remove the previous container from docker desktop or by using the following commands
```
docker stop rm-test
docker rm rm-test
```
