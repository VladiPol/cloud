import logging
import datetime as dt
import pandas as pd

import azure.functions as func


def main(mytimer: func.TimerRequest, doc: func.Out[func.Document]) -> None:
    utc_timestamp = dt.datetime.utcnow().replace(
        tzinfo=dt.timezone.utc).isoformat()

    ###########################
    # Custom code BEGIN       #
    ###########################
      
    # get info from web site
    df_COVID_Wiki = pd.read_html('https://de.wikipedia.org/wiki/COVID-19-Pandemie_in_Deutschland', decimal=',', thousands='.')    
    
    # parse HTML and convert the data into JSON-String
    day = (dt.datetime.now().strftime('%Y%m%d'))
    df_COVID_BUND_JSON = df_COVID_Wiki[2].to_json(force_ascii=False)

    # finalize the JSON-String and put the result into CosmosDB        
    doc.set(func.Document.from_json('{"id":"'+(day)+'",' + df_COVID_BUND_JSON[1:-1] +'}'))

    ###########################
    # Custom code END         #
    ###########################


    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
