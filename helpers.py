from datetime import datetime
import requests

def getUserInput():
    """For interactive usage, will prompt the user to make a choice."""
    choice = str(input("Do you want me to attempt (Yes/No/Exit)? :: "))
    while choice.lower() not in ['yes', 'no', 'exit']:
        choice = str(input("Sorry, type Yes or No or Exit :: "))
    return choice.lower()

def validateapiEndPoint(endpoint):
    """Pass the end point url. Will only result in true if the endpoint is hosted locally"""
    # put some code here to check that the given url is not malicious
    # Here I am just checking if this url contains localhost or not
    return 'localhost' in endpoint

def logMessage(msg_text, log_level):
    """Takes a string as input, appends datetime stamp and writes to stdout"""
    print(f"{log_level}: {datetime.now()} {msg_text} \n")

def extractPortInfo(data):
    """Takes the response Json, Parses it and returns Port info"""
        # pickout if there is any ports info in the json
    try:
        hostport = data["config"]["ports"][0]["hostPort"]
        containerport = data["config"]["ports"][0]["containerPort"]
        return True, hostport, containerport

    except KeyError:
        logMessage("Port information is not available, container will be created but its services will not be available externally", "WARNING")
        return False, "", ""

def makeApiRequest(endpoint):
    """Takes an end point as input and tries retreiving data by making an API call. Pass the endpoint URL as input. It will return true and the response data if successful OR returns false and the error message"""
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            return True, response.json()
    except requests.exceptions.ConnectionError:
        return False, "Connection_Error"
    except requests.exceptions.Timeout:
        return False, "Request_Timed_Out"
    except requests.exceptions.TooManyRedirects:
        return False, "Too_Many_Redirects"
    except requests.exceptions.JSONDecodeError:
        return True, "Request is successful, but a blank response has been received"
    except requests.exceptions.RequestException as e:
        return False, f"There is an error making this call. Check that the end point is online. error is {str(e)}"
    

def getMessageAndWriteToFile(hostport, data):
    """ Pass hostport and the initial API call response in Json format. Ouputs a file"""
    endpoint = f"http://localhost:{hostport}{data['endpoint']}"

    status, response = makeApiRequest(endpoint)
    if not status:
        logMessage(f"API call to the end point {data['endpoint']} failed, does it exist? check Dockerfile for the image", "ERROR")

    else:
        # We have response OK, ready to compose the file
        env_params = data['config']['environment']

        # The env dictionary from conversation-app may/can contain more than one key, value pair
        # Match this to the message from the newly spun up container

        try:
            msg_to_be_written = response['message'] + env_params["SAY_" + response['message'].upper().strip() + "_TO"]
        except KeyError:
            logMessage(f"The new container end point did not seem to have sent the message we are looking for. It sent {response['message']}", "WARNING")
            exit()
        if msg_to_be_written != "":
            # Write into a file 
            with open("output.log", "a") as out_file:
                out_file.write(f'{msg_to_be_written}\n')
                logMessage(f"output is written to the file {out_file.name}", "INFO")
        else:
            logMessage("No output file produced by this process", "WARNING")