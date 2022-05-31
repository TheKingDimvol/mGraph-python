import uuid


class Base:
    driver = None

    def __init__(self):
        self.session = None
        self.tx = None

    @classmethod
    def close(cls):
        cls.driver.close()

    @classmethod
    def add_uuid(cls, params):
        params['uuid'] = str(uuid.uuid4())

    @classmethod
    def execute_query_single(cls, query, **params):
        with cls.driver.session() as session:
            result = session.run(query, params=params)
            record = result.single()
            if record:
                record = record.data()
                if 'params' in record:
                    params = record.pop('params')
                    if 'title' in params:
                        params['label'] = params.pop('title')
                    record = record | params
        return record

    @classmethod
    def execute_query(cls, query, **params):
        with cls.driver.session() as session:
            result = session.run(query, params=params)
            data = result.data()
            for record in data:
                if 'params' in record:
                    params = record.pop('params')
                    if 'title' in params:
                        params['label'] = params.pop('title')
                    for k, v in params.items():
                        record[k] = v
        return data

    def start_transaction(self):
        self.session = self.driver.session()
        self.tx = self.session.begin_transaction()
        return self.tx

    def close_transaction(self):
        self.tx.commit()
        self.tx.close()
        self.session.close()

