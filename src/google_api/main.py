from controllers import gmail_controller
from models import gmail_api

if __name__ == '__main__':
    # gmail_controller.send_gmail_attach_file()
    ga = gmail_api.GmailApi()
    receives = ga.receive_gmail(3, query='test aaa bbb')

    if receives:
        for receive in receives:
            print(receive['Received'])
            print(receive['Delivered-To'])
            print(receive['snippet'])
            print('-' * 20)
    else:
        print('msg: No search results')
    # ga.receive_gmail_threads()
