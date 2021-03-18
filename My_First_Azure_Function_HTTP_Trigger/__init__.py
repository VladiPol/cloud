import logging
import time
import datetime as dt
import pandas as pd
import json

import azure.functions as func

def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ###########################
    # Custom code BEGIN       #
    ###########################

    # just get the currently server time
    ctime = time.ctime()
    
    # get info from web site
    df_COVID_Wiki = pd.read_html('https://de.wikipedia.org/wiki/COVID-19-Pandemie_in_Deutschland', decimal=',', thousands='.')    
    df_COVID_BUND = df_COVID_Wiki[2]

    day = (dt.datetime.now().strftime('%Y%m%d'))
    df_COVID_BUND_JSON = df_COVID_BUND.to_json(force_ascii=False)

    ###########################
    # Custom code END         #
    ###########################

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        # write to CosmosDB --> test
        # doc.set(func.Document.from_dict({"id":"3","bundesland":"BE","anzahl_gesamt":1973,"anzahl_100T":53.8,"tendenz_vortag": -0.9,}))        
        
        # put df_COVID_BUND into CosmosDB        
        doc.set(func.Document.from_json('{"id":"'+(day)+'",' + df_COVID_BUND_JSON[1:-1] +'}')) 

        # make formatted string
        response = (
            #f"Hello, <b>{name}</b>. The currently server time is {ctime}. This HTTP triggered function executed successfully.\n\n"
            f"Hello, {name}. The currently server time is {ctime}. This HTTP triggered function executed successfully.\n\n"
            f"COVID-19 7-Tage-Inzidenz der Bundesländer:\n"
            f"{df_COVID_BUND}"            
        )
        #return func.HttpResponse(f"Hello, {name}. The currently server time is {ctime}. This HTTP triggered function executed successfully.\n\n {df_COVID_BUND}")
        #return func.HttpResponse(f"{response}", mimetype="text/html")
        return func.HttpResponse(f"{response}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
