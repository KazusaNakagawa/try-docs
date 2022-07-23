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
        user_id = input('Please select the processing user by number\n')
        logger.info({
            'msg': 'Selected UserID',
            'user_id': user_id,
        })
        try:
            user_id = int(user_id)
        except ValueError as _:
            msg = 'Please select by number\n'
            print(msg)
            logger.info({
                'msg': 'msg',
                'user_id': user_id,
            })
            continue
        if user_id > len(users) or user_id < 1:
            print('Out of selection, please select again')
            continue
        break

    logger.info({'msg': 'End Select users to be processed'})
    return user_id

