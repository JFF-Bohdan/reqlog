import mock
from reqlog.support.datatablessupport import BaseAdapter, DataTablesParser, DataTablesResponse
from reqlog.support.datatablessupport.datatablessupport import DataTableParserSupportFunctions

from .dataforparsing import VALID_DATA_FOR_PARSING


def test_returns_valid_results_on_valid_input():
    expected_columns_data = [
        "added_at",
        "uid",
        "dcd_name",
        "dcn_name",
        "method",
        "params_count",
        "event_details_href_data"
    ]

    result = DataTablesParser.parse(VALID_DATA_FOR_PARSING, FakeRequestAdapter)

    assert result is not None
    assert result.columns_count == 7
    assert result.filter_by(mask=None) == "abc"

    all_columns_data = result.all_columns_data()
    assert all_columns_data is not None
    assert type(all_columns_data) == list
    assert all_columns_data == expected_columns_data

    assert result.order_by() == "added_at asc"
    assert result.low_level_order_by() == [("added_at", "asc")]

    for index in range(result.columns_count):
        assert result.column_data(index) == expected_columns_data[index]


def test_parser_can_find_middle_value_in_string_for_columns_tasks():
    data_strings = [
        "columns[0][data]",
        "columns[0][name]",
        "columns[0][searchable]",
        "columns[0][orderable]",
        "columns[0][search][value]",
        "columns[0][search][regex]",
    ]

    expected_values = [
        "data",
        "name",
        "searchable",
        "orderable",
        "value",
        "regex"
    ]

    for index, task in enumerate(data_strings):
        value = DataTableParserSupportFunctions.find_middle_value(task, "columns\[.*\]\[", "\].*")
        assert expected_values[index] == value


def test_parser_can_find_middle_value_in_string_for_search_tasks():
    data_strings = [
        "columns[0][search][value]",
        "columns[0][search][regex]"
    ]

    expected_values = [
        "value",
        "regex"
    ]

    for index, task in enumerate(data_strings):
        value = DataTableParserSupportFunctions.find_middle_value(task, "columns\[.*\]\[.*\]\[", "\].*")
        assert expected_values[index] == value


def test_parser_can_find_middle_value_in_string_for_order_tasks():
    data_strings = [
        "order[0][column]",
        "order[0][dir]"
    ]

    expected_values = [
        "column",
        "dir"
    ]

    for index, task in enumerate(data_strings):
        value = DataTableParserSupportFunctions.find_middle_value(task, "order\[[^\[\]]\]\[", "\].*")
        assert expected_values[index] == value


def test_response_produces_valid_json():
    fake_data = {
        "foo": "bar",
        "bizz": "bazz"
    }

    expected_draw = 200
    expected_records_filtered = 111
    expected_records_total = 222

    resp = DataTablesResponse.produce_result(fake_data, expected_draw, expected_records_filtered, expected_records_total)
    assert resp is not None

    assert "data" in resp
    assert resp["data"] == fake_data

    assert "draw" in resp
    assert resp["draw"] == expected_draw

    assert "recordsTotal" in resp
    assert resp["recordsTotal"] == expected_records_total

    assert "recordsFiltered" in resp
    assert resp["recordsFiltered"] == expected_records_filtered


def test_response_produces_valid_json_when_data_field_name_():
    fake_data = {
        "foo": "bar",
        "bizz": "bazz"
    }

    expected_draw = 200
    expected_records_filtered = 111
    expected_records_total = 222

    field_name = "zoom_zoom"

    resp = DataTablesResponse.produce_result(
        fake_data,
        expected_draw,
        expected_records_filtered,
        expected_records_total,
        field_name
    )
    assert resp is not None

    assert field_name in resp
    assert resp[field_name] == fake_data

    assert "draw" in resp
    assert resp["draw"] == expected_draw

    assert "recordsTotal" in resp
    assert resp["recordsTotal"] == expected_records_total

    assert "recordsFiltered" in resp
    assert resp["recordsFiltered"] == expected_records_filtered


def test_support_returns_none_when_converting_to_int_invalid_values():
    assert DataTableParserSupportFunctions.convert_to_integer("ABC") is None


def test_support_returns_specified_value_when_converting_to_int_invalid_values():
    assert DataTableParserSupportFunctions.convert_to_integer("ABC", "FOO") == "FOO"


def test_support_returns_correct_value_when_converting_to_int_valid_value():
    assert DataTableParserSupportFunctions.convert_to_integer("123") == 123


def test_calls_logger_when_specified(mocker):
    logger = mock.Mock()
    method = mocker.patch.object(logger, "error")

    DataTableParserSupportFunctions.safe_log_error(logger, "msg")

    method.assert_called_once_with("msg")


class FakeRequestAdapter(BaseAdapter):
    def __init__(self, request):
        super().__init__(request)

    def get_all_keys(self):
        return self.request.keys()

    def get_value(self, field_name, field_default_value=None):
        return self.request.get(field_name, field_default_value)
