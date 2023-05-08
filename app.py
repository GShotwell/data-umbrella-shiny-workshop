from shiny import App, render, ui
import pandas as pd

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider(
                id="mass",
                label="Max Body Mass",
                min=2000,
                max=8000,
                value=3000,
            )
        ),
        ui.panel_main(ui.h2("Palmer Penguins"), ui.output_table(id="summary")),
    )
)


def server(input, output, session):
    df = pd.read_csv("penguins.csv")

    @output
    @render.table
    def summary():
        out = df.copy()
        out = out.loc[df["Body Mass (g)"] < input.mass()]
        out = out.groupby("Species", as_index=False).size()
        return out


app = App(app_ui, server)
