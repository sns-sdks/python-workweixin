"""
    参数校验
"""
from pywework.error import ErrorCode, WeWorkError


def incompatible_validator(**kwargs):
    """
    Validate the incompatible parameters.
    Args:
        kwargs (str)
            Parameter need to do validate.
    Returns:
        None
    """
    given = 0
    for name, param in kwargs.items():
        if param is not None:
            given += 1
    params = ",".join(kwargs.keys())
    if given == 0:
        raise WeWorkError(ErrorCode.MISSION_PARAM, f"Specify at least one of {params}")
    elif given > 1:
        raise WeWorkError(
            ErrorCode.INVALID_PARAM, f"Incompatible parameters specified for {params}"
        )
