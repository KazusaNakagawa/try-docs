from controllers import gmail_controller
from models import gmail_api

if __name__ == '__main__':
    # gmail_controller.send_gmail_attach_file()
    ga = gmail_api.GmailApi()
    receives = ga.receive_gmail(10, query='')

    if receives:
        for receive in receives:
            print('jst_time: ', receive['jst_time'])
            print('From: ', receive['From'])
            print('To: ', receive['To'])
            print('Subject: ', receive['Subject'])
            print('snippet: ', receive['snippet'][0:50])
            print('-' * 20)
    else:
        print('msg: No search results')
    # ga.receive_gmail_threads()
