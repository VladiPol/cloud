import logging
import time
import datetime as dt
import pandas as pd

import azure.functions as func


def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ###########################
    # Custom code BEGIN       #
    ###########################

    # just get the currently server time and day for Cosmos DB
    ctime = time.ctime()
    day = (dt.datetime.now().strftime('%Y%m%d'))
    
    # get info from web site
    df_Wiki = pd.read_html('https://de.wikipedia.org/wiki/COVID-19-Impfung_in_Deutschland', decimal=',', thousands='.')
    df_Impfung = df_Wiki[1]

    # erste Impfung in Deutschland %
    df_Impf_1 = df_Impfung.iloc[18, df_Impfung.columns.get_level_values(1)=='erste Impfung']
    # zweite Impfung in Deutschland %
    df_Impf_2 = df_Impfung.iloc[18, df_Impfung.columns.get_level_values(1)=='vollst. Impfung']
    # Strip the string and convert it into integer
    out_1 = df_Impf_1[1].replace(u'\xa0%', u'').replace(',','.')
    out_2 = df_Impf_2[1].replace(u'\xa0%', u'').replace(',','.')
    out_1 = float(out_1)
    out_2 = float(out_2)

    # build JSON for Input into CosmosDB
    out_JSON = '{"id":"' + (day) + '",' + '"BRD erste Impfung PCT":' + str(out_1) + ',"BRD zweite Impung PCT":' + str(out_2) + '}'

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

        # put Imp. Information into CosmosDB
        doc.set(func.Document.from_json(out_JSON))

        # make formatted string
        response = (
            f"Hello, {name}. The currently server time is {ctime}. This HTTP triggered function executed successfully.\n\n"
            f"COVID-19 7-Tage-Inzidenz der Bundesländer:\n"
            f"{out_JSON}"            
        )
        return func.HttpResponse(f"{response}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
