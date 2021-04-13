from typing import Dict, Sequence, Tuple, Union

import pytest
from _pytest.mark.structures import MarkDecorator, ParameterSet

__all__ = ["Config", "make_params"]


class Config:
    def __init__(
        self,
        id: str,
        *,
        new_cmds: Union[str, Sequence[str]],
        legacy_cmds: Union[str, Sequence[str]],
        passed: int = 0,
        skipped: int = 0,
        failed: int = 0,
        errors: int = 0,
        xpassed: int = 0,
        xfailed: int = 0,
    ):
        self._id = id
        self._new_cmds = self._parse_cmds(new_cmds)
        self._legacy_cmds = self._parse_cmds(legacy_cmds)
        self._outcomes: Dict[str, int] = dict(
            passed=passed,
            skipped=skipped,
            failed=failed,
            errors=errors,
            xpassed=xpassed,
            xfailed=xfailed,
        )

    @staticmethod
    def _parse_cmds(cmds: Union[str, Sequence[str]]) -> Tuple[str, ...]:
        return (cmds,) if isinstance(cmds, str) else tuple(cmds)

    @staticmethod
    def _amend_cmds(cmds: Tuple[str, ...], file: str) -> Tuple[str, ...]:
        if not cmds or not cmds[0].startswith(":"):
            return (file, *cmds)
        else:
            return (file + cmds[0], *cmds[1:])

    def make_params(self, file: str) -> Tuple[ParameterSet, ...]:
        return (
            pytest.param(
                file,
                self._amend_cmds(self._new_cmds, file),
                self._outcomes,
                id=f"{self._id}-new",
            ),
            pytest.param(
                file,
                self._amend_cmds(self._legacy_cmds, file),
                self._outcomes,
                id=f"{self._id}-legacy",
            ),
        )


def make_params(file: str, *configs: Config) -> MarkDecorator:
    return pytest.mark.parametrize(
        ("file", "cmds", "outcomes"),
        [param for config in configs for param in config.make_params(file)],
    )
