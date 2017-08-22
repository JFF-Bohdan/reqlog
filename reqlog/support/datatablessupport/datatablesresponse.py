class DataTablesResponse(object):
    def __init__(self):  # pragma: no coverage
        pass

    @staticmethod
    def produce_result(data, draw, records_filtered, records_total, data_field_name="data"):
        return {
            data_field_name: data,
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered
        }
