import azure.functions as func
import datetime
import json
import logging
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient
from azure.appconfiguration import  AzureAppConfigurationClient, ConfigurationSetting
from azure.appconfiguration.provider import load, SettingSelector
import os

app = func.FunctionApp()

def get_config_client():
    connstr =  os.getenv("APPCONFIG_CONNECTION_STRING")
    return AzureAppConfigurationClient.from_connection_string(connstr)

def load_config():
    connstr =  os.getenv("APPCONFIG_CONNECTION_STRING")
    return load(connection_string=connstr)


@app.route(route="send_message", auth_level=func.AuthLevel.ANONYMOUS)
def send_message(req: func.HttpRequest) -> func.HttpResponse:
    logging.debug('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid message", status_code=402)

    logging.info("--- body ---")
    logging.info(req_body)


    queue_name = "taskqueue"
    account_url = "https://az204cg001.queue.core.windows.net"
    credential = DefaultAzureCredential()

    queue = QueueClient(account_url=account_url, queue_name=queue_name, credential=credential) 

    msg = req_body.get("message", None)
    if not msg:
        config = get_config_client()
        msg = config.get_configuration_setting(key="FunctionApp:DefaultMessage")
        #msg = load_config()["FunctionApp:DefaultMessage"]

    receipt = queue.send_message(msg)
    receipt = queue.send_message(msg)
    receipt = queue.send_message(msg)

    messages = queue.receive_messages(max_messages=10)

    result = []

    #for page in messages.by_page():
    #    for message in page:
    if True:
        for message in messages:
            print("--- ", message.content)
            result.append(message.content)
            queue.delete_message(message)

    if not receipt:
        logging.info("No receipt received")

    return func.HttpResponse(json.dumps({"messages": result}), status_code=201)
