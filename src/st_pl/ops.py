from typing import TypeVar
import polars as pl
import polars.selectors as cs

DF = TypeVar("DF", pl.DataFrame, pl.LazyFrame)


def mutate(df: DF, x: dict[str, pl.Expr]) -> DF:
    return df.with_columns(**x)


def subset(df: DF, row: pl.Expr, col: pl.Expr = cs.all()) -> DF:
    return df.select(col).filter(row)


def summarize(df: DF, grp: list | pl.Expr, agg_fn: dict[str, pl.Expr]) -> DF:
    return df.group_by(grp).agg(**agg_fn)
