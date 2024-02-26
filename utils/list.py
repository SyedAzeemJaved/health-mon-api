def return_list_of_ids(db_result: tuple[str | None]) -> list[int]:
    """Return a list of int ids from by formatting or parsing the string received from the database"""
    _ids = db_result[0]

    if _ids is None:
        return []

    return [int(x) for x in _ids.split(",")]
