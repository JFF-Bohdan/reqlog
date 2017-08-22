from .datatablesparseddata import DataTablesParsedData
from .datatablesparseddatavalidator import DataTablesParsedDataValidator
from .datatablessupport import DataTableParserSupportFunctions


class DataTablesParser(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(request, adapter_cls, logger=None):
        request_adapter = adapter_cls(request)
        res = DataTablesParsedData()

        keys = list(request_adapter.get_all_keys())
        res = DataTablesParser._read_columns_attributes_and_update_parsed_data(request_adapter, res, keys, logger)
        if res is None:
            return None

        res = DataTablesParser._get_start_index_and_update_parsed_data(request_adapter, res, logger)
        if res is None:
            return None

        res = DataTablesParser._get_length_and_update_parsed_data(request_adapter, res, logger)
        if res is None:
            return None

        res = DataTablesParser._read_ordering_for_columns_and_update_parsed_data(request_adapter, res, keys, logger)

        if res is None:
            return None

        res.search_value = request_adapter.get_value("search[value]", "")
        res.search_reg_ex = DataTableParserSupportFunctions.scan_boolean(request_adapter.get_value("search[regex]"))
        if res.search_reg_ex is None:
            DataTableParserSupportFunctions.safe_log_error(logger, "non boolean value in search[regex]")
            return None

        res.draw = DataTableParserSupportFunctions.convert_to_integer(request_adapter.get_value("draw"))

        if not DataTablesParser._check_valid(res, logger):
            return None

        return res

    @staticmethod
    def _read_columns_attributes_and_update_parsed_data(request_adapter, res, keys, logger=None):
        keys = [key for key in keys if key.startswith("columns")]

        # parsing strings like 'columns[1][data]' and 'columns[1][search][regex]'
        for k in keys:
            column_index = DataTablesParser._get_column_index(k, "columns")

            if column_index is None:
                DataTableParserSupportFunctions.safe_log_error(logger, "column index is None for column '{0}".format(k))
                return None

            column_attribute = DataTableParserSupportFunctions.find_middle_value(k, "columns\[.*\]\[", "\].*")
            if column_attribute is None:
                DataTableParserSupportFunctions.safe_log_error(
                    logger,
                    "column attribute is not specified for column '{0}'".format(k)
                )
                return None

            if column_attribute == "search":
                # parsing strings like 'columns[1][search][regex]', retrieving second attribute
                additional_attribute = DataTableParserSupportFunctions.find_middle_value(
                    k,
                    "columns\[.*\]\[.*\]\[", "\].*"
                )

                if additional_attribute is None:
                    DataTableParserSupportFunctions.safe_log_error(
                        logger,
                        "column additional attribute is None for 'search' column '{0}'".format(k)
                    )
                    return None

                column_attribute = column_attribute + "-" + additional_attribute

            column_parameters = res.columns[column_index] if column_index in res.columns else {}
            # retrieving value
            value = request_adapter.get_value(k, None)

            column_parameters[column_attribute] = value
            res.columns[column_index] = column_parameters

        return res

    @staticmethod
    def _get_integer_attribute_value(request_adapter, attribute_name, logger=None):
        # retrieving start index
        v = request_adapter.get_value(attribute_name)
        v = DataTableParserSupportFunctions.convert_to_integer(v, None)
        if v is None:
            DataTableParserSupportFunctions.safe_log_error(
                logger,
                "'{}' parameter is not specified".format(attribute_name)
            )
            return None

        return v

    @staticmethod
    def _get_start_index_and_update_parsed_data(request_adapter, res, logger=None):
        res.start = DataTablesParser._get_integer_attribute_value(request_adapter, "start", logger)
        if res.start is None:
            return None

        return res

    @staticmethod
    def _get_length_and_update_parsed_data(request_adapter, res, logger=None):
        res.length = DataTablesParser._get_integer_attribute_value(request_adapter, "length", logger)
        if res.length is None:
            return None

        return res

    @staticmethod
    def _read_ordering_for_columns_and_update_parsed_data(request_adapter, res, keys, logger=None):
        keys = [key for key in keys if key.startswith("order")]

        # parsing strings like 'columns[1][data]' and 'columns[1][search][regex]'
        for k in keys:
            column_index = DataTablesParser._get_column_index(k, "order")

            if column_index is None:
                DataTableParserSupportFunctions.safe_log_error(
                    logger,
                    "column index is not specified for 'order' column '{0}'".format(k)
                )
                return None

            column_attribute = DataTableParserSupportFunctions.find_middle_value(k, "order\[[^\[\]]\]\[", "\].*")
            if column_attribute is None:
                DataTableParserSupportFunctions.safe_log_error(
                    logger,
                    "column atribute is not specified for 'order' column '{0}'".format(k)
                )
                return None

            # adding new column parameter with value
            if column_index in res.ordering:
                column_parameters = res.ordering[column_index]
            else:
                column_parameters = {}

            # retrieving value
            value = request_adapter.get_value(k)

            column_parameters[column_attribute] = value
            res.ordering[column_index] = column_parameters

        return res

    @staticmethod  # noqa: C901 #'DataTablesParser._check_valid' is too complex (17)
    def _check_valid(parsed_data, logger=None):
        return DataTablesParsedDataValidator.check(parsed_data, logger)

    @staticmethod
    def _get_column_index(value, prefix):
        v = DataTableParserSupportFunctions.find_middle_value(value, "{0}\[".format(prefix), "\].*")
        if v is None:
            return None

        v = str(v).strip()
        if not v.isnumeric():
            return None

        return int(v)
