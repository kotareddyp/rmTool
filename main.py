import requests
import os
import time
# from datetime import datetime

from helpers import getUserInput, validateapiEndPoint, logMessage, makeApiRequest, getMessageAndWriteToFile
from container import runContainer, containerIsHealthy

if __name__ == "__main__":
    # get the user input and bail if the choice is no or exit
    # Comment this out if we are not going to take user input
    choice = getUserInput()
    if choice in ["no", "exit"]:
        exit()
    start = time.time()
    # what is the conversation app endpoint? if it is not set as env use a known default value
    apiEndPoint = os.getenv("apiURL", "http://localhost:6161/api/applications/conversation-app")
    # We need to check if this url is actually correct i.e. is it locally available?
    if not validateapiEndPoint(apiEndPoint):
        logMessage(f"Given end point {apiEndPoint} is not valid.. exiting", "ERROR")
        exit()
    logMessage(f"Querying end point : {apiEndPoint}", "INFO")
    # URL seems ok, proceed to make the call
    success, response = makeApiRequest(apiEndPoint)
    if not success:
        logMessage(f"failed when making the API call to {apiEndPoint}, error is {response}", "ERROR")

    # Pass the response object to spin up a new container
    status, hostport = runContainer(response)

    if not status:
        # bail, cotainer creation failed
        logMessage("Issue when creating container, check above log messages", "INFO")
        exit()

    # We have a container, is it healthy though?
    if containerIsHealthy(hostport):
    # Now hit the end point on the new container and collect data
        getMessageAndWriteToFile(hostport, response)
        
    # To calculate time taken
    end = time.time()
    logMessage(f"INFO: This process took {end-start} seconds", "INFO")