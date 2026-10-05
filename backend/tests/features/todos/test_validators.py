from datetime import date

import pytest
from pydantic import ValidationError

from app.features.todos.schemas import TodoCreate, TodoUpdate
from app.features.todos.validators import validate_patch_fields, validate_title


def test_rejects_an_empty_patch():
    with pytest.raises(ValidationError, match="Provide at least one field"):
        TodoUpdate()


@pytest.mark.parametrize("field", ["title", "description", "priority", "completed"])
def test_rejects_explicit_null_for_non_nullable_fields(field):
    with pytest.raises(ValidationError, match=f"Field {field} cannot be null"):
        TodoUpdate(**{field: None})


def test_allows_clearing_only_the_due_date():
    patch = TodoUpdate(due_date=None)
    assert validate_patch_fields(patch) is patch
    assert patch.model_dump(exclude_unset=True) == {"due_date": None}


def test_preserves_every_non_null_patch_field():
    patch = TodoUpdate(
        title="  Renamed task  ", description="  Details  ", priority="low",
        completed=False, due_date="2026-10-15",
    )
    assert validate_patch_fields(patch) is patch
    assert patch.model_dump(exclude_unset=True) == {
        "title": "Renamed task", "description": "Details", "priority": "low",
        "completed": False, "due_date": date(2026, 10, 15),
    }


@pytest.mark.parametrize("title", ["Line\none", "Line\rone", "Line\r\none"])
@pytest.mark.parametrize("model, kwargs", [(TodoCreate, {}), (TodoUpdate, {})])
def test_rejects_multiline_titles_in_create_and_update(model, kwargs, title):
    with pytest.raises(ValidationError, match="must be a single line"):
        model(title=title, **kwargs)


def test_trims_surrounding_newlines_before_checking_title():
    assert TodoCreate(title="\n Plan \n").title == "Plan"


def test_allows_newlines_in_description():
    assert TodoCreate(title="Plan", description="a\nb").description == "a\nb"


def test_validate_title_passes_through_none_and_single_line():
    assert validate_title(None) is None
    assert validate_title("Plan") == "Plan"
