from helpers import logMessage, extractPortInfo, makeApiRequest
import docker
import time

def runContainer(data):

    """Input is the JSON object from the request and outputs the status and the hostport number for further use"""
        # check if the required image is tagged
    if ":" in data['image']:
        requested_image = data['image']
    else:
        # Assume latest image
        requested_image = data['image'] + ":latest"
    logMessage(f"Requested image is : {requested_image}", "INFO")

    try:
    #    instantiate
        logMessage(f"Initialising docker client \U0001F605", "INFO")
        d_client = docker.from_env()
    #   search for the requeste image
        requested_image = d_client.images.get(data['image'] + ":latest")
    except docker.errors.ImageNotFound:
        logMessage("image is not found on this host's local image repository", "ERROR")
        exit()
    except docker.errors.APIErro:
        logMessage("Unable to get Docker profile on this host", "ERROR")
        exit()
    
    # Lets see what port spec is available
    port_info, hostport, containerport = extractPortInfo(data)
    try:
        if port_info:
            ports = {containerport:hostport}
            logMessage("Starting to run a container from this image", "INFO")
            # Instantiate the container
            new_container = d_client.containers.run(requested_image, detach=True, ports=ports, name='rm-test')
        else:
            new_container = d_client.containers.run(requested_image, detach=True, name='rm-test')
                # phew.. there werent any errors with the container
            logMessage(f"Container {new_container} is created successfully", "INFO")
        return (True, hostport)
    except docker.errors.ContainerError:
        logMessage("A container was created but exited with an error", "ERROR")
        exit()
    except docker.errors.ImageNotFound:
        logMessage("Requested image is no more in the registry", "WARNING")
        exit()
    except docker.errors.APIError:
        logMessage("Image instantiation failed, see docker logs for more info", "ERROR")
        exit()
    

def containerIsHealthy(hostport):
    """Takes hostport as input and makes call to the endpoint to check health status. Returns true or false"""
    # Test if the container is working and serving
    status = ""
    tries = 0
    # Give 10 tries and bailout
    out_string = 'waiting for the new container \U0001F612'
    logMessage(out_string, "INFO")
    while status != "OK" or tries < 5:
        # Try and see if the new container's end point is up
        health_ep = f"http://localhost:{hostport}/health"
        tries += 1
        # Exponential backoff
        time.sleep(2*tries)
        out_string = out_string + " ."
        logMessage(out_string, "INFO")
        status, response = makeApiRequest(health_ep)
        if status:
            status = "OK"
            break
        if response in ["Connection_Error", "Request_Timed_Out"]:
            logMessage('New container is not ready yet.. waiting \U0001F612', "INFO")
        
    if status != "OK":
        logMessage("New container did not respond before timeout!", "WARNING")
        exit()

    logMessage("Container instance is healthy, ready and working" + "\U0001F601", "INFO")
    return True
