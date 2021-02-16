import logging
import time
import pandas as pd

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ###########################
    # Custom code comms here  #
    ###########################

    # just get the currently server time
    ctime = time.ctime()
    
    # get info from web site
    df_COVID_Wiki = pd.read_html('https://de.wikipedia.org/wiki/COVID-19-Pandemie_in_Deutschland', decimal=',', thousands='.')    
    df_COVID_BUND = df_COVID_Wiki[3]

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        # make formatted string
        response = (
            f"Hello, {name}. The currently server time is {ctime}. This HTTP triggered function executed successfully.\n\n"
            f"COVID-19 7-Tage-Inzidenz der Bundesländer:\n"
            f"{df_COVID_BUND}"
        )
        #return func.HttpResponse(f"Hello, {name}. The currently server time is {ctime}. This HTTP triggered function executed successfully.\n\n {df_COVID_BUND}")
        return func.HttpResponse(f"{response}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
