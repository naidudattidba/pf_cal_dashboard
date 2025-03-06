import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
from salary import Salary
from pf import PFCalculator
from future_pf import FuturePF

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Provident Fund (PF) Calculator Dashboard", style={'textAlign': 'center'}),

    # User Input Fields
    html.Div([
        html.Label("Basic Salary (₹)"),
        dcc.Input(id="salary", type="number", value=50000, style={"width": "100%"}),
        
        html.Label("Existing PF Balance (₹)"),
        dcc.Input(id="existing_pf", type="number", value=200000, style={"width": "100%"}),
        
        html.Label("Years of Contribution"),
        dcc.Input(id="years", type="number", value=10, style={"width": "100%"}),
        
        html.Label("Annual Salary Hike (%)"),
        dcc.Input(id="hike", type="number", value=5, style={"width": "100%"}),
        
        html.Button("Calculate PF", id="calculate-btn", n_clicks=0, style={"marginTop": "10px"}),
    ], style={"width": "50%", "margin": "auto", "padding": "20px", "border": "1px solid black", "borderRadius": "10px"}),

    # Output Summary
    html.Div(id="output-summary", style={"marginTop": "20px", "textAlign": "center", "fontSize": "18px"}),

    # Graphs
    html.Div([
        dcc.Graph(id="pf-line-graph"),  # Line Graph
        dcc.Graph(id="pf-bar-graph"),   # Bar Graph
    ])
])

# Callback to calculate and update results
@app.callback(
    [Output("output-summary", "children"), 
     Output("pf-line-graph", "figure"), 
     Output("pf-bar-graph", "figure")],
    [Input("calculate-btn", "n_clicks")],
    [State("salary", "value"), State("existing_pf", "value"),
     State("years", "value"), State("hike", "value")]
)
def update_dashboard(n_clicks, salary, existing_pf, years, hike):
    if n_clicks == 0:
        return "", px.scatter(), px.scatter()  # No graph before clicking

    # Convert hike percentage to decimal
    hike = hike / 100  

    # Calculate PF projection
    salary_obj = Salary(salary)
    pf_calculator = PFCalculator(salary_obj)
    future_pf = FuturePF(pf_calculator, existing_pf, years, hike)
    df = future_pf.calculate_future_pf()

    # Summary Text
    summary = f"Projected PF Balance after {years} years: ₹{df['Total PF Balance'].iloc[-1]:,.2f}"

    # Create Line Graph (Total PF Balance over Years)
    line_fig = px.line(df, x="Year", y="Total PF Balance", 
                       title="Projected PF Growth Over Time",
                       labels={"Year": "Years", "Total PF Balance": "PF Balance (₹)"},
                       markers=True)

    # Create Bar Graph (Annual PF Contribution per Year)
    bar_fig = px.bar(df, x="Year", y="Annual PF", 
                     title="Annual PF Contribution Over Time",
                     labels={"Year": "Years", "Annual PF": "Yearly PF Contribution (₹)"},
                     text_auto=True)

    return summary, line_fig, bar_fig

# Run Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
