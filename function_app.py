import azure.functions as func
import datetime
import json
import logging
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient

app = func.FunctionApp()

@app.route(route="send_message", auth_level=func.AuthLevel.ANONYMOUS)
def send_message(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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

    receipt = queue.send_message(req_body['message'])
    receipt = queue.send_message(req_body['message'])
    receipt = queue.send_message(req_body['message'])

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
