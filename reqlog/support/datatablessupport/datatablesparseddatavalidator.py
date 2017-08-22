from .datatablessupport import DataTableParserSupportFunctions


class DataTablesParsedDataValidator(object):
    def __init__(self):  # pragma: no coverage
        pass

    @staticmethod
    def check(parsed_data, logger=None):
        if parsed_data.length == 0:
            DataTableParserSupportFunctions.safe_log_error(logger, "'length' is not specified")
            return False

        keys = sorted(list(parsed_data.columns.keys()))
        if not DataTablesParsedDataValidator._check_indexes(keys, logger):
            return False

        if not DataTablesParsedDataValidator._check_for_mandatory_attributes(parsed_data, keys, logger):
            return False

        if not DataTablesParsedDataValidator._check_that_ordering_attributes_valid(parsed_data, logger):
            return False

        return True

    @staticmethod
    def _check_indexes(keys, logger=None):
        previous = None

        for key in keys:
            if previous is None:
                if int(key) != 0:
                    DataTableParserSupportFunctions.safe_log_error(logger, "first index is not '0'")
                    return False

                previous = key
                continue

            if previous + 1 != int(key):
                DataTableParserSupportFunctions.safe_log_error(logger, "wrong indexes sequence")
                return False

            previous = key

        return True

    @staticmethod
    def _check_for_mandatory_attributes(parsed_data, keys, logger):
        # checking for valid parameters
        for k in keys:
            params = parsed_data.columns[k]

            if "data" not in params:
                DataTableParserSupportFunctions.safe_log_error(
                    logger,
                    "'data' parameter is not specified for column '{0}'".format(k)
                )
                return False

        return True

    @staticmethod
    def _check_that_ordering_attributes_valid(parsed_data, logger):
        order_keys = sorted(list(parsed_data.ordering.keys()))
        if len(order_keys) == 0:
            return True

        minIndex = order_keys[0]
        maxIndex = order_keys[-1]
        colsCount = parsed_data.columns_count

        if (minIndex < 0) or (minIndex >= colsCount):
            DataTableParserSupportFunctions.safe_log_error(logger, "Wrong index in ordering")
            return False

        if (maxIndex < 0) or (maxIndex >= colsCount):
            DataTableParserSupportFunctions.safe_log_error(logger, "Wrong index in ordering")
            return False

        # checking all attributes for each order entry
        for k in order_keys:
            attrs = parsed_data.ordering[k]

            # retrieving column index
            if "column" not in attrs:
                DataTableParserSupportFunctions.safe_log_error(logger, "No 'column' attribute in ordering part")
                return False

            column_index = DataTablesParsedDataValidator._scan_numeric(attrs["column"])
            if column_index is None:
                DataTableParserSupportFunctions.safe_log_error(logger, "Wrong column index in ordering part")
                return False

            if (column_index < 0) or (column_index >= colsCount):
                DataTableParserSupportFunctions.safe_log_error(logger, "Wrong target index in ordering part")
                return False

            # retrieving direction
            if "dir" not in attrs:
                DataTableParserSupportFunctions.safe_log_error(logger, "No 'dir' attribute in ordering part")
                return False

            direction = str(attrs["dir"]).strip().lower()

            if direction not in ["asc", "desc"]:
                DataTableParserSupportFunctions.safe_log_error(logger, "Wrong order direction in ordering part")
                return False

        return True

    @staticmethod
    def _scan_numeric(value):
        if value is None:
            return None

        if not str(value).isnumeric():
            return None

        return int(value)
