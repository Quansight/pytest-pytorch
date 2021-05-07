from typing import Collection, List, Optional, Sequence, Set, Tuple, Union

import pytest
from _pytest.mark.structures import MarkDecorator, ParameterSet

__all__ = ["Config", "make_params", "make_parametrization"]


class Config:
    PARAM_NAMES = ("file", "cmds", "selection")

    def __init__(
        self,
        *,
        file: Optional[str] = None,
        new_cmds: Union[str, Sequence[str]] = (),
        legacy_cmds: Optional[Union[str, Sequence[str]]] = None,
        selection: Collection[str],
    ):
        self._file = file
        self._new_cmds = new_cmds
        if legacy_cmds is None:
            legacy_cmds = new_cmds
        self._legacy_cmds = legacy_cmds
        self._selection = selection

    @staticmethod
    def _parse_cmds(cmds: Union[str, Sequence[str]], file: str) -> Tuple[str, ...]:
        cmds = (cmds,) if isinstance(cmds, str) else tuple(cmds)
        if not cmds or not cmds[0].startswith("::"):
            return (file, *cmds)
        else:
            return (file + cmds[0], *cmds[1:])

    @staticmethod
    def _parse_selection(selection: Collection[str], file: str) -> Set[str]:
        return {file + item if item.startswith("::") else item for item in selection}

    @staticmethod
    def _cmds_to_id(cmds: Tuple[str, ...]) -> str:
        return " ".join(cmds)

    def make_params(self, file: Optional[str] = None) -> Tuple[ParameterSet, ...]:
        file = self._file or file
        if not file:
            raise pytest.UsageError

        new_cmds = self._parse_cmds(self._new_cmds, file)
        legacy_cmds = self._parse_cmds(self._legacy_cmds, file)
        selection = self._parse_selection(self._selection, file)

        new_params = pytest.param(
            file,
            new_cmds,
            selection,
            id=self._cmds_to_id(new_cmds),
        )
        if new_cmds == legacy_cmds:
            return (new_params,)

        legacy_cmds = pytest.param(
            file,
            legacy_cmds,
            selection,
            id=self._cmds_to_id(legacy_cmds),
        )

        return (new_params, legacy_cmds)


def make_params(*configs: Config, file: Optional[str] = None) -> List[ParameterSet]:
    return [param for config in configs for param in config.make_params(file)]


def make_parametrization(*configs, file: Optional[str] = None) -> MarkDecorator:
    return pytest.mark.parametrize(Config.PARAM_NAMES, make_params(*configs, file=file))
