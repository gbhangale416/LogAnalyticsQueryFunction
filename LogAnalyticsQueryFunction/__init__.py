import logging
import datetime
import LogAnalyticsQuery.LogAnalyticsQuery as QL



import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    logging.info('The timer is past due! Started to execute function')
    QL.LogAnalyticsQuery()

    logging.info('Python timer trigger function ran at %s', utc_timestamp)


