class DataTablesParsedData(object):
    def __init__(self):
        self.columns = {}
        self.start = 0
        self.length = 0

        self.ordering = {}
        self.search_reg_ex = False
        self.search_value = ""
        self.draw = ""
        self._calculated_columns_count = None

    @property
    def columns_count(self):
        """
        Returns columns count
        :return: columns count
        """
        if self._calculated_columns_count is not None:
            return self._calculated_columns_count

        max_index = max([int(key) for key in self.columns.keys()], default=None)
        self._calculated_columns_count = max_index + 1 if max_index is not None else 0

        return self._calculated_columns_count

    def filter_by(self, mask=(lambda x: "%" + x + "%")):
        """
        Returns filter by rule
        :param mask: lamda or function which must be used for filter rule decoration
        :return: filter by rule
        """
        if self.search_value is None:
            return None

        v = str(self.search_value).strip()
        if len(v) == 0:
            return None

        if not mask:
            return v

        return mask(v)

    def column_attribute(self, column_index, attribute_name):
        """
        Returns attribute for column
        :param column_index: column index
        :param attribute_name: attribute name
        :return: attribute value for column
        """
        attrs = self.column_attributes(column_index)
        if attrs is None:
            return None

        if attribute_name not in attrs:
            return None

        return attrs[attribute_name]

    def column_attributes(self, column_index):
        if column_index not in self.columns:
            return None

        return self.columns[column_index]

    def column_data(self, column_index):
        """
        Returns `data` attribute for column
        :param column_index: column index
        :return: `data` attribute value for column
        """
        return self.column_attribute(column_index, "data")

    def all_columns_data(self, remove_empty=True):
        """
        Returns all requested columns list (values of `data` attribute for each column

        :param remove_empty: remove columns with no `data` attribute specified
        :return: requested columns list
        """
        ret = []
        for i in range(self.columns_count):
            val = self.column_data(i)
            if remove_empty and (len(val) == 0):
                continue

            ret.append(val)

        return ret

    def _columns_data(self):
        ret = []

        # looking for names and indexes
        for k in self.columns.keys():
            params = self.columns[k]

            if "data" in params:
                ret.append((k, params["data"]))

        # sorting by index
        ret = sorted(ret, key=lambda entry: entry[0])

        # filtering only names
        xret = []
        for (index, name, ) in ret:
            xret.append(name)

        return xret

    def low_level_order_by(self, name_mappings=None, filter_not_mapped=False):
        ret = []

        if (name_mappings is None) and filter_not_mapped:
            return ret

        keys = list(self.ordering.keys())
        keys = sorted(keys)

        for k in keys:
            attrs = self.ordering[k]

            if "column" not in attrs:
                return None

            column_index = int(attrs["column"])
            request_column_name = str(self.column_data(column_index)).strip()

            if len(request_column_name) == 0:
                continue

            if(name_mappings is not None) and (request_column_name in name_mappings):
                columnName = name_mappings[request_column_name]
            else:
                if filter_not_mapped:
                    continue

                columnName = request_column_name

            if "dir" not in attrs:
                return None

            order_direction = str(attrs["dir"])

            item = (columnName, order_direction)
            ret.append(item)

        return ret

    def order_by(self, name_mappings=None, filter_not_mapped=False):
        """
        Returns array of field names and sorting type (asc/desc)

        :param name_mappings: Map of field names for sorting, if field name differs in Db and in DataTable
            actual Db must be mapped there. If field name same in Db and in DataTable it can be skipped in mapping.
        :param filter_not_mapped:
        :return:
        """

        data = self.low_level_order_by(name_mappings, filter_not_mapped)
        if data is None:
            return None

        ret = []
        for (column, order_direction) in data:
            item = column
            order_direction = str(order_direction).strip()

            if len(order_direction) > 0:
                item += " " + order_direction

            ret.append(item)

        return ", ".join(ret)
