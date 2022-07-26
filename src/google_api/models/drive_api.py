from models.client_service import ClientService


class DriveApi(ClientService):

    def __init__(self):
        super().__init__()
        self.service = self.get_service_drive_v3()
