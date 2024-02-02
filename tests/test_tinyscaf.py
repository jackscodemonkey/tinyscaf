"""
This is a test template file
"""

import pathlib
from unittest.mock import patch, mock_open

import pytest
import tempfile
from jinja2 import Environment, FileSystemLoader
from tinyscaf.tinyscaf import (
    find_config,
    get_templates,
    write_file,
    handle_user_choice,
)


def test_find_config():
    mock_path = pathlib.Path("/mock/directory")
    mock_config_file = mock_path / "tinyscaf.json"

    # Mock Path.cwd() to return the mock_path
    with patch("pathlib.Path.cwd", return_value=mock_path):
        # Mock Path.rglob to find the mock config file
        with patch("pathlib.Path.rglob", return_value=iter([mock_config_file])):
            result = find_config()
            assert (
                result == mock_config_file
            ), "The returned path should be the mock path"


def test_find_config_file_not_found():
    mock_path = pathlib.Path("/mock/directory")

    with patch("pathlib.Path.cwd", return_value=mock_path):
        with patch("pathlib.Path.rglob", return_value=iter([])):
            with pytest.raises(FileNotFoundError) as excinfo:
                find_config()
            assert "tinyscaf.json file not found under path:" in str(excinfo.value)


def test_get_templates_with_files():
    mock_template_dir = pathlib.Path("/mock/template/directory")
    mock_templates = [
        mock_template_dir / "template1.jinja",
        mock_template_dir / "template2.jinja",
    ]

    with patch("pathlib.Path.glob", return_value=mock_templates):
        result = get_templates(mock_template_dir)
        assert (
            list(result) == mock_templates
        ), "The function should return all .jinja files"


def test_get_templates_no_files():
    mock_template_dir = pathlib.Path("/mock/template/directory")

    with patch("pathlib.Path.glob", return_value=[]):
        with pytest.raises(FileNotFoundError) as excinfo:
            get_templates(mock_template_dir)
        assert f"No templates found at: {mock_template_dir}" in str(excinfo.value)


def test_write_file(mocker):
    # Prepare the template content and the expected output
    template_content = "Hello, {{ name }}!"
    answers = {"name": "John Snow"}
    expected_output = "Hello, John Snow!"

    # Mock open to avoid actual file operations
    m = mock_open(read_data=template_content)
    mocker.patch("builtins.open", m)

    # Mock FileSystemLoader and Environment to control template loading
    mocker.patch.object(
        Environment,
        "get_template",
        return_value=mocker.Mock(render=lambda answers: expected_output),
    )

    # Prepare the template and output file paths
    template_file = pathlib.Path("/fake/path/template.txt")
    out_file = pathlib.Path("/fake/path/output.txt")

    # Call the function under test
    write_file(template_file, out_file, answers)

    # Ensure the file was written to with the expected content
    m.assert_called_once_with(out_file, "w")  # Check if open was called correctly
    handle = m()
    handle.write.assert_called_once_with(expected_output)  # Verify the write operation


def test_handle_user_choice_valid():
    items = ["apple", "banana", "cherry"]
    choice = 2
    assert (
        handle_user_choice(choice, items) == "banana"
    ), "Should return the item corresponding to the choice"


def test_handle_user_choice_float_integer():
    items = ["apple", "banana", "cherry"]
    choice = 2.0  # Float but should be treated as an integer 2
    assert (
        handle_user_choice(choice, items) == "banana"
    ), "Should handle float that represents an integer"


def test_handle_user_choice_out_of_range():
    items = ["apple", "banana", "cherry"]
    choice = 5  # Out of range
    assert (
        handle_user_choice(choice, items) is None
    ), "Should return None for choices out of range"
