import serial
import time
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from tkinter import Tk, filedialog

# === User-Defined Interval (in seconds) ===
INTERVAL_SECONDS = 5  # Change this value to set the interval

# === Choose File Save Location ===
Tk().withdraw()  # Hide the Tkinter root window
file_path = filedialog.asksaveasfilename(
    defaultextension=".xlsx",
    filetypes=[("Excel files", "*.xlsx"), ("All Files", "*.*")],
    title="Choose save location"
)

print(f"Data will be saved to: {file_path}")

# === Initialize serial connection ===
ser = serial.Serial('COM3', 115200, timeout=1)  # Ensure COM5 is correct
time.sleep(2)  # Allow time for the connection to stabilize

# === Initialize Dash app ===
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='graph-update', interval=1000, n_intervals=0)
])

# === Data storage ===
times = []
temp1_data = []
temp2_data = []
start_time = time.time()

# === Excel DataFrame Initialization ===
df = pd.DataFrame(columns=["Time (s)", "Sensor 1 (°C)", "Sensor 2 (°C)"])
last_save_time = time.time()


@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph(n):
    global last_save_time

    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            temp1, temp2 = map(float, line.split(','))
            temp1 -= 7  # Subtract 7°C from Temperature 2
            current_time = time.time() - start_time

            # Append data
            times.append(current_time)
            temp1_data.append(temp1)
            temp2_data.append(temp2)

            # Update the DataFrame
            df.loc[len(df)] = [current_time, temp1, temp2]

            # === Save to Excel every INTERVAL_SECONDS ===
            if time.time() - last_save_time >= INTERVAL_SECONDS:
                df.to_excel(file_path, index=False)
                print(f"Data saved to Excel at {round(current_time, 2)} seconds.")
                last_save_time = time.time()

            # === Plot the graph ===
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=times, y=temp1_data, mode='lines', name='Sensor 1 (°C)'))
            fig.add_trace(go.Scatter(x=times, y=temp2_data, mode='lines', name='Sensor 2 (°C)'))

            # Set the axis ranges and start at 0,0
            fig.update_layout(
                title="Real-Time Temperature Monitoring",
                xaxis_title="Time (s)",
                yaxis_title="Temperature (°C)",
                legend_title="Sensors",
                xaxis=dict(range=[0, max(times) + 5], zeroline=True),
                yaxis=dict(range=[0, max(max(temp1_data), max(temp2_data)) + 5], zeroline=True)
            )
            return fig
        except ValueError:
            pass


# === Run the app ===
if __name__ == '__main__':
    app.run(port=8050)