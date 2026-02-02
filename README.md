This is typical my data workflow which include validation, skim, transform, table, dashboard.

### create a task
task = MyTask(filename="a.csv", shape=(14, 12))  # type: ignore
task.load(pl.read_csv, has_header=True)
task.filter(pl.col("mpg") > 20)

assert task, "\x1b[31mfail task shape check\x1b[0m"
task.info
task.data.describe()

if task.check_row(pl.col("am").is_in([0, 1])):
    print("test pass")

try:
    task.app.run()
except KeyboardInterrupt:
    print("\nShiny app stopped by user.")

### data manipulation
df = task.data 

a1 = {"var1": pl.col("mpg") / 10, "var2": (pl.col("mpg") > 25).not_()}
mutate(df, a1)

a2 = (pl.col("hp") > 200) | (pl.col("car").str.contains("Mer|^F"))
a3 = cs.matches("m|p") | cs.string()
subset(df, a2, a3)

a4 = ["carb"]
a5 = {"mpg_mean": pl.col("mpg").mean().round(2), "n_num": pl.len()}
summarize(df, a4, a5)

res = df.pipe(mutate, x=a1).pipe(subset, row=a2).pipe(summarize, grp=a4, agg_fn=a5)
print(res)


