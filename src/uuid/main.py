import uuid

for _ in range(2):
    uuid_ = {'UUID': uuid.UUID,
             'uuid4': uuid.uuid4(),
             # 'uuid3': uuid.uuid3('name', 'name2'),
             # 'uuid2': uuid.uuid(),
             'uuid1': uuid.uuid1(),
             'NAMESPACE_DNS': uuid.NAMESPACE_DNS,
             'uuid5': uuid.uuid5(uuid.NAMESPACE_DNS, "datasette.ios")
             }

    # print(uuid_['NAMESPACE_DNS'])
    # print(uuid_['uuid4'])
    # print(uuid_['uuid1'])
    # print(uuid_['UUID'])
    print(uuid_['uuid5'])
    print(uuid_['NAMESPACE_DNS'])
