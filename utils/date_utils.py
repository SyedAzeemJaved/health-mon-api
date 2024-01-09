from datetime import datetime


CREATED_AND_UPDATED_AT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    """Convert datetime to ISO 8601 format with the Z suffix"""
    return dt.strftime(CREATED_AND_UPDATED_AT_FORMAT)


def get_current_datetime_in_str_iso_8601_with_z_suffix() -> str:
    """Get current datetime in ISO 8601 format with the Z suffix"""
    return datetime.utcnow().strftime(CREATED_AND_UPDATED_AT_FORMAT)
