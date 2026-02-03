import argparse
import polars as pl

from .ops import mutate, subset, summarize
from .task import MyTask

__all__ = ["mutate", "subset", "summarize", "MyTask"]


# st_plcli /mnt/c/Users/Stewart\ Li/Desktop/tbd/a.csv --shape 32 12
def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="path to the target csv")
    parser.add_argument(
        "--shape",
        nargs=2,
        type=int,
        metavar=("ROWS", "COLS"),
        required=True,
        help="expected shape of the data (rows cols)",
    )

    args = parser.parse_args()
    task = MyTask(filename=args.filename, shape=tuple(args.shape))
    task.load(pl.read_csv)
    print(task.data.describe())
