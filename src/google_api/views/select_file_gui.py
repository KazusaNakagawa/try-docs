import PySimpleGUI as sg

from const import PY_SIMPLE_GUI
from config.log_conf import LogConf


def select_file_gui() -> str:
    logger = LogConf().get_logger(__file__)
    logger.info({'msg': 'Start Select users to be processed'})

    sg.theme(PY_SIMPLE_GUI['theme'])
    layout = [[sg.Text('Enter files to comare')],
              [sg.Text('File', size=(8, 1)), sg.Input(), sg.FilesBrowse()],
              [sg.Submit(), sg.Cancel()]]
    window = sg.Window('File Compare', layout, font=PY_SIMPLE_GUI['font'])

    try:
        event, values = window.read()
        logger.info({
            'event': event,
            'select values': values,
        })

        window.close()
        return values[0].split(";")

    except Exception as ex:
        # TODO: Add Slack Alert
        logger.error({
            'msg': 'An unexpected exception occurred. Processing will be stopped.',
            'ex': ex,
        })
        raise Exception
