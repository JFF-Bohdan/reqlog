import re


class DataTableParserSupportFunctions:
    def __init__(self):  # pragma: no coverage
        pass

    @staticmethod
    def convert_to_integer(value, defaultValue=None):
        if value is None:
            return None

        if not str(value).isnumeric():
            return defaultValue

        return int(value)

    @staticmethod
    def find_middle_value(value, prefix, suffix):
        pattern = "{}(.+?){}".format(prefix, suffix)
        m = re.search(pattern, value)

        if not m:
            return None

        found = m.group(1)
        return found

    @staticmethod
    def db_bool_to_bool(value):
        if value is None:
            return False

        if not str(value).isnumeric():
            return False

        if int(value) != 0:
            return True

        return False

    @staticmethod
    def scan_boolean(value):
        if value is None:
            return False

        value = str(value)
        if value.isnumeric():
            return DataTableParserSupportFunctions.db_bool_to_bool(value)

        value = value.lower()

        if value == "true":
            return True

        return False

    @staticmethod
    def safe_log_error(logger, message):
        if not logger:
            return

        logger.error(message)


class BaseAdapter(object):
    def __init__(self, request=None):  # pragma: no coverage
        self.request = request

    def get_all_keys(self):
        pass

    def get_value(self, field_name, field_default_value=None):
        pass


class DataTablesBottleRequestAdapter(BaseAdapter):
    def __init__(self, request):
        super().__init__(request)

    def get_all_keys(self):
        return self.request.params.keys()

    def get_value(self, field_name, field_default_value=None):
        return self.request.params.get(field_name, field_default_value)


class DataTablesFlaskRequestAdapter(BaseAdapter):
    def __init__(self, request):
        super().__init__(request)

    def get_all_keys(self):
        return list(self.request.values.keys())

    def get_value(self, field_name, field_default_value=None):
        return self.request.values.get(field_name, field_default_value)
