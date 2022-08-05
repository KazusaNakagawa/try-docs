import PySimpleGUI as sg

from const import PY_SIMPLE_GUI
from config.log_conf import LogConf


def select_send_gmail_gui(users: list) -> int:
    """Select users to be processed

    :param
      users(list): List of users registered in the spreadsheet

    :return:
      user_id(int): Target User No.
    """
    logger = LogConf().get_logger(__file__)
    logger.info({'msg': 'Start Select users to be processed'})

    user_account_names = [f"{user['id']}: {user['account_name']}" for idx, user in enumerate(users)]

    sg.theme(PY_SIMPLE_GUI['theme'])
    # All the stuff inside your window.
    layout = [
        [sg.Text('Select Account Name')],
        [sg.Combo(user_account_names)],
        [sg.Button('Ok'), sg.Button('Cancel')]
    ]

    # Create the Window
    window = sg.Window(
        title='Select Send Gmail Account', layout=layout, font=PY_SIMPLE_GUI['font'], size=(400, 300), resizable=True
    )
    # Event Loop to process "events" and get the "values" of the inputs
    try:
        while True:
            event, values = window.read()
            # if user closes window or clicks cancel
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            event, user_id = 'You entered ', values[0].split(':')[0]
            if user_id.isnumeric():
                logger.info({
                    'event': event,
                    'select user_id': user_id,
                })
                window.close()
                # Adjust spreadsheet get rows by -1
                logger.info({'msg': 'End Select users to be processed'})
                return int(user_id) - 1

    except Exception as ex:
        # TODO: Add Slack Alert
        logger.error({
            'msg': 'An unexpected exception occurred. Processing will be stopped.',
            'ex': ex,
        })
        raise Exception
