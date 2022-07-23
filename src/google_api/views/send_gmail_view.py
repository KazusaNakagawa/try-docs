from src.google_api.config.log_conf import LogConf


def send_gmail_select_user_console(users: list) -> int:
    """ Select users to be processed

    :param
      users(list): List of users registered in the spreadsheet

    :return:
      user_id(int): Target User No.
    """
    logger = LogConf().get_logger(__file__)
    logger.info({'msg': 'Start Select users to be processed'})

    for idx, user in enumerate(users):
        print(f"{idx + 1}: {user['account_name']}")

    while True:
        try:
            user_id = input('Please select the processing user by number\n')
            logger.info({
                'msg': 'Selected UserID',
                'user_id': user_id,
            })
            if not user_id.isnumeric():
                msg = 'Please select by number\n'
                print(msg)
                logger.info({
                    'msg': msg,
                    'user_id': user_id,
                })
                continue
            user_id = int(user_id)
            if user_id > len(users) or user_id < 1:
                msg = 'Out of selection, please select again\n'
                print(msg)
                logger.info({
                    'msg': msg,
                    'user_id': user_id,
                })
                continue
            break

        except Exception as ex:
            # TODO: Add Slack Alert
            logger.error({
                'msg': 'An unexpected exception occurred. Processing will be stopped.',
                'ex': ex,
            })
            raise Exception

    logger.info({'msg': 'End Select users to be processed'})
    # starting number 0. Adjustment of the acquisition number of the spreadsheet
    return user_id - 1
