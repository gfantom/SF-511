# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests as r
from typing import Tuple

app = Flask(__name__)

def parse_511_payload(*stop_codes: Tuple[int]) -> str:
    toJoin = []

    for arg in stop_codes:
        re = r.get("https://proxy-prod.511.org/api-proxy/api/v1/transit/stop/?stopcode=" + str(arg))
        re_dict = re.json()["Routes"][0]["Routes"]

        for i in re_dict:
            toJoin.append( """  {} - {}
  arriving in: {}
""".format( i["Code"], i["DirectionName"], ", ".join(i["Departures"]) ) )

    return "\n".join(toJoin)
        
@app.route("/", methods=['GET'])
def default():
    return "Hello World!"

@app.route("/sms", methods=['POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # getting the response body
    stop_codes = request.data.decode("utf-8").split(" ")
    stop_code_ints = [int(i) for i in stop_codes]

    resp_body = parse_511_payload( *stop_code_ints )
    
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message( resp_body )

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
