from shiny import App, render, ui, reactive
import pandas as pd
from plotnine import ggplot, geom_density, aes, theme_light


app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider(
                id="mass",
                label="Max Body Mass",
                min=2000,
                max=8000,
                value=6000,
            ),
            ui.input_action_button("reset", "Reset Slider"),
        ),
        ui.panel_main(
            ui.h2("Palmer Penguins"),
            ui.output_table(id="summary"),
            ui.output_plot(id="mass_hist"),
        ),
    )
)


def server(input, output, session):
    df = pd.read_csv("penguins.csv")

    @reactive.Calc
    def filtered_data():
        filt_df = df.copy()
        filt_df = filt_df.loc[df["Body Mass (g)"] < input.mass()]
        return filt_df

    @output
    @render.table
    def summary():
        out = filtered_data().groupby("Species", as_index=False).size()
        return out

    @output
    @render.plot
    def mass_hist():
        plot_df = filtered_data()
        plot = (
            ggplot(plot_df, aes(x="Body Mass (g)", fill="Species"))
            + geom_density(alpha=0.2)
            + theme_light()
        )
        return plot

    @reactive.Effect
    @reactive.event(input.reset)
    def _():
        print("Pushed!")
        ui.update_slider(id="mass", value=6000)


app = App(app_ui, server)
