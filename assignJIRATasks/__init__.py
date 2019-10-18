import datetime
import logging
import time
import datetime as d
import azure.functions as func

from jira import JIRA
from textblob.classifiers import NaiveBayesClassifier


user_name = 'sysbitbucket'
password = '2aTn3rB[PR"utt'
jira = ''
train = []
start_time = time.time()
options = {'server': 'http://jira.hm.com'}


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
        logging.info('Starting the trigger***************************************')
        
    trigger_jira()
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
# Jira Server Connection
# Authentication


def trigger_jira() -> None:
    try:
        jira = JIRA(options, basic_auth=(f'{user_name}', f'{password}'))

    except BaseException as Be:
        logging.exception("******************************start*************************************")
        logging.exception(Be)
        logging.exception("********************************end***********************************")

    logging.info("-----------------------------------------------------------")
    all_closed_issues = jira.search_issues(
        'project = "HAAL Support" AND status in (resolved, closed) AND assignee is not EMPTY ORDER BY createdDate ASC',
        maxResults=False)
    logging.info("-----------------------------------------------------------")
    logging.info(len(all_closed_issues))
    for i in range(0, len(all_closed_issues)):
        logging.info(all_closed_issues[i].key)
        train.append((str(all_closed_issues[i].key.split('-')[0]) + ' ' + str(all_closed_issues[i].fields.summary),
                      all_closed_issues[i].fields.assignee.name))

    cl = NaiveBayesClassifier(train)

    all_open_issues = jira.search_issues(
        'project = "HAAL Support" AND status=open AND assignee = EMPTY', maxResults=False
    )
    if len(all_open_issues) > 0:
        for i in range(0, len(all_open_issues)):
            issue = str(all_open_issues[i].key.split('-')[0]) + \
                    ' ' + str(all_open_issues[i].fields.summary)
            assignee_ = cl.classify(issue)
            logging.info(all_open_issues[i].key,
                         ' can be assigned to : ', assignee_)
            jira.assign_issue(all_open_issues[i].key, assignee_)
            total_time_lapse = time.time() - start_time
            logging.info(f"--- Total Time:  {total_time_lapse} seconds ---")
    else:
        cur_date = d.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info("There aren't any issues to be assigned. will try again in a 10 minute.(" + cur_date + ")")
        

if __name__ == '__main__':
    trigger_jira()

