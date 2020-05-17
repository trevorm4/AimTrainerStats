import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from utils import *
from stats import *
import yaml
import plotly.express as px

config = yaml.load(open("config.yaml","r"))
app = dash.Dash(__name__)
df = init_df()
if len(df.index) == 0:
    index_folder(df,config["directory"])
mean_df = create_mean_df(df)
app.layout = html.Div(
    className="",
    children=[
        html.Div(
            className="dropdowns-div",
            style={},
            children=[
            dcc.Dropdown(
                id="graph-scenario-dropdown",
                options=[
                    { "label" : x, "value" : x} for x in df["Scenario"].unique()
                ],
                style={
                    "width" : "40%",
                    "display" : "inline-block",
                    "float" : "left"
                },
                value=df["Scenario"].unique()[0]
            ),
            dcc.Dropdown(
                id="graph-type-dropdown",
                options=[
                    { "label" : x, "value" : x} for x in ["Score","Accuracy"]
                ],
                style={
                    "width" : "40%",
                    "float" : "left",
                    "margin-left" : "-18rem"
                },
                value="Score"
            ),
            html.H3(children="Fly's KovaaK's Dashboard",style={"margin-left" : "-30rem"})
            ]
        ),
        html.Div(
            className="graphs-div",
            style={"clear" : "left"},
            children=[
                dcc.Graph(id="scenario-graph")
            ]
        ),
        html.Div(
            className="table-div",
            style={"width" : "50%", "margin" : "auto"},
            children=[
                dcc.DatePickerRange(
                    id='date-picker',
                    min_date_allowed=df.index.min(),
                    max_date_allowed=df.index.max(),
                    initial_visible_month=df.index.max(),
                    start_date=df.index.min(),
                    end_date=df.index.max()
                ),
                dash_table.DataTable(id="table",
                                     columns=[{"name": i, "id": i} for i in ["Date"] + list(df.columns)],
                                     style_as_list_view=True,
                                     style_cell={"font-family" : "tahoma"}
                                     )

            ]
        )

    ]
)
@app.callback(
    Output("scenario-graph","figure"),
    [Input("graph-scenario-dropdown","value"),Input("graph-type-dropdown","value")]
)
def create_graph(scenario,metric):
    sub_df = mean_df[mean_df["Scenario"] == scenario]
    fig = px.line(sub_df,x="Date",y=metric)
    fig.update_layout(
        title=f"{scenario} {metric}",
        xaxis_title="Date",
        yaxis_title=metric
    )
    return fig

@app.callback(
    Output("table","data"),
    [Input("graph-scenario-dropdown","value"),Input("date-picker","start_date"),Input("date-picker","end_date")]
)
def create_table(scenario,start_date, end_date):
    temp_df = df.reset_index()
    temp_df = temp_df[(temp_df["Scenario"] == scenario) & (temp_df["index"] >= start_date) & (temp_df["index"] <= end_date)]
    temp_df["index"] = temp_df["index"].dt.strftime("%m-%d-%y %H:%M:%S")
    temp_df = temp_df.sort_values("index",ascending=False)
    return temp_df.rename(columns={"index" : "Date"}).to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)