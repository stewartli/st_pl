from typing import Any
import polars as pl
from shiny import App
from pydantic import BaseModel, FilePath

from .dash import creat_app  # type: ignore[reportMissingImports]


class MyTask(BaseModel):
    filename: FilePath
    shape: tuple[int, int]
    _data: pl.DataFrame | None = None

    def __bool__(self) -> bool:
        return self.data.shape == self.shape

    def load(self, f, **kwargs) -> None:
        if self._data is None:
            self._data = f(self.filename, **kwargs)

    def filter(self, x: pl.Expr) -> None:
        self._data = self.data.filter(x)

    @property
    def data(self) -> pl.DataFrame:
        if self._data is None:
            raise RuntimeError("call load() to read data in")
        return self._data

    def check_row(self, x: pl.Expr) -> bool:
        return self.data.filter(x).height > 0

    @property
    def info(self) -> dict[str, Any]:
        return {
            "file": self.filename.name,
            "size": self.filename.stat().st_size,
            "dim": self.data.shape,
        }

    @property
    def app(self) -> App:
        return creat_app(self.data)
