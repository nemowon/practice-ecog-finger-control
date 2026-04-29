import streamlit as st
from scipy.io import loadmat
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Get random samples from the cue stage
def get_random_stage_samples(stage_data, segment_length, n_samples=1, random_state=None):
    n_full_segments = len(stage_data) // segment_length
    if n_full_segments == 0:
        raise ValueError("Not enough rows in stage_data for a single segment.")

    rng = np.random.default_rng(random_state)
    selected_indices = rng.choice(n_full_segments, size=min(n_samples, n_full_segments), replace=False)

    segments = [
        stage_data.iloc[i * segment_length:(i + 1) * segment_length].reset_index(drop=True)
        for i in selected_indices
    ]
    return segments, selected_indices

sub1 = loadmat("data/sub1_comp.mat")
# good_ch_1 = find_good_channels(sub1['train_data'], sub1['train_dg'], "Subject 1")

train_data = pd.DataFrame(sub1['train_data'][::4])  # Downsample 1000 Hz -> 250 Hz
train_dg = pd.DataFrame(sub1["train_dg"][::4])      # Downsample 1000 Hz -> 250 Hz
fs = 250
cue_duration = 2
rest_duration = 2
cycle_duration = cue_duration + rest_duration

samples_per_cycle = cycle_duration * fs # 1000
samples_per_state = cue_duration * fs # 500

num_rows = train_data.shape[0]
num_cycles = train_data.shape[0] // samples_per_cycle
num_channels = train_data.shape[1]
num_dg_channels = train_dg.shape[1]

# Segment the data into cycles
train_data['trial_id'] = np.arange(num_rows) // samples_per_cycle
train_data['is_rest'] = (np.arange(num_rows) % samples_per_cycle) // samples_per_state
train_dg['trial_id'] = np.arange(num_rows) // samples_per_cycle
train_dg['is_rest'] = (np.arange(num_rows) % samples_per_cycle) // samples_per_state

# Cue stage data
cue_ecog = train_data[train_data['is_rest'] == 0]
cue_dg = train_dg[train_dg['is_rest'] == 0]

# Rest stage data
rest_ecog = train_data[train_data['is_rest'] == 1]
rest_dg = train_dg[train_dg['is_rest'] == 1]

random_stage_samples, random_stage_indices = get_random_stage_samples(cue_ecog, samples_per_state, n_samples=1)
print("Random cue stage sample indices:", random_stage_indices)
random_stage_sample = random_stage_samples[0]
print("Random cue stage sample shape:", random_stage_sample.shape)

st.title("🧠 :rainbow[Brain Behind the Bot] 🦾")
st.write("ECoG to Robotic Arm Simulation")

# Create slider to control animation
n_frames = min(random_stage_sample.shape[0], 50)  # Reduce frames for faster animation
frame_step = max(1, random_stage_sample.shape[0] // n_frames)

# Build animated figure with Plotly
fig = go.Figure()

# Add traces for each channel with animation frames
frames = []
for i in range(0, random_stage_sample.shape[0], frame_step):
    frame_data = []
    for ch in random_stage_sample.columns:
        frame_data.append(
            go.Scatter(
                x=np.arange(i + 1),
                y=random_stage_sample[ch].iloc[:i + 1],
                mode='lines',
                name=f'Ch {ch}'
            )
        )
    frames.append(go.Frame(data=frame_data))

# Initial frame - show first frame data
first_frame_data = frames[0].data if frames else []
for trace in first_frame_data:
    fig.add_trace(trace)

fig.frames = frames
fig.update_layout(
    updatemenus=[{
        'type': 'buttons',
        'showactive': False,
        'x': 0.5,
        'y': 1.15,
        'xanchor': 'center',
        'yanchor': 'top',
        'buttons': [
            {'label': 'Send Random Test ECoG channels to model', 'method': 'animate', 'args': [None, {'frame': {'duration': 10, 'redraw': True}, 'fromcurrent': True, 'mode': 'immediate'}]}
        ]
    }],
    xaxis_title='Downsampled Time',
    yaxis_title='ECoG Signal',
    height=400,
    hovermode='x unified',
    xaxis=dict(range=[0, samples_per_state])
)

st.plotly_chart(fig, width='stretch')

