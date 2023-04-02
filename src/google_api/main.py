from controllers import gmail_controller
from models import gmail_api
from models import custom_search_api


def main_receive_gmail_test():
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


def main_custom_search():
    csa = custom_search_api.CustomSearchApi()
    csa.get_search_response('ダイエット')


if __name__ == '__main__':
    # gmail_controller.send_gmail_attach_file()
    # main_receive_gmail_test()
    main_custom_search()
