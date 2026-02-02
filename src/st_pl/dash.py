import io
import polars as pl
from shiny import App, ui, render


def creat_app(df: pl.DataFrame) -> App:
    app_ui = ui.page_fluid(
        ui.tags.style("""
        #show_data {
            border-top: 6px solid red;
        }
        """),
        ui.h3("MyTask Data Viewer"),
        ui.download_button(
            "download_csv",
            "Download CSV",
            class_="btn-primary",
        ),
        ui.div(
            ui.output_data_frame("show_data"),
            style="""
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 8px;
                background-color: #f9f9f9;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
                shiny-datagrid-table-top-border: 6px solid red
            """,
        ),
    )

    def server(input, output, session):
        @render.data_frame
        def show_data():
            return render.DataTable(
                df,
                width="100%",
                height="600px",
                selection_mode="rows",
                filters=True,
                editable=True,
            )

        @render.download(filename="data.csv")
        def download_csv():
            with io.StringIO() as buf:
                df.write_csv(buf)
                yield buf.getvalue()

    return App(app_ui, server)
