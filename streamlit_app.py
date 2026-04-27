import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Process Monitoring Tool", layout="wide")

st.title("Sampling-Based Process Monitoring Tool using the Central Limit Theorem")

st.write("""
This interactive tool simulates process data and shows how sample means can be used
to monitor a process. It applies the Central Limit Theorem and adds control limits
to identify possible out-of-control conditions.
""")

# Sidebar
st.sidebar.header("Simulation Settings")

distribution = st.sidebar.selectbox(
    "Choose process distribution:",
    ["Uniform", "Exponential", "Normal"]
)

sample_size = st.sidebar.slider(
    "Sample size (n):",
    min_value=2,
    max_value=100,
    value=10
)

num_samples = st.sidebar.slider(
    "Number of samples:",
    min_value=100,
    max_value=10000,
    value=1000,
    step=100
)

shift_process = st.sidebar.checkbox("Introduce process shift")

shift_amount = 0
if shift_process:
    shift_amount = st.sidebar.slider(
        "Shift amount:",
        min_value=-30,
        max_value=30,
        value=10
    )

population_size = 100000

# Generate process data
if distribution == "Uniform":
    population = np.random.uniform(0, 100, population_size)

elif distribution == "Exponential":
    population = np.random.exponential(scale=10, size=population_size)

else:
    population = np.random.normal(loc=50, scale=10, size=population_size)

# Apply shift if selected
if shift_process:
    population = population + shift_amount

# Generate sample means
sample_means = []

for i in range(num_samples):
    sample = np.random.choice(population, size=sample_size)
    sample_means.append(np.mean(sample))

sample_means = np.array(sample_means)

# Control limits
center_line = np.mean(sample_means)
std_error = np.std(sample_means)
ucl = center_line + 3 * std_error
lcl = center_line - 3 * std_error

out_of_control_points = np.where((sample_means > ucl) | (sample_means < lcl))[0]
num_out_of_control = len(out_of_control_points)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Process Distribution")
    fig1, ax1 = plt.subplots()
    ax1.hist(population, bins=50, edgecolor="black")
    ax1.set_xlabel("Process Value")
    ax1.set_ylabel("Frequency")
    st.pyplot(fig1)

with col2:
    st.subheader("Distribution of Sample Means")
    fig2, ax2 = plt.subplots()
    ax2.hist(sample_means, bins=50, edgecolor="black")
    ax2.axvline(center_line, linestyle="--", label="Center Line")
    ax2.axvline(ucl, linestyle="--", label="UCL")
    ax2.axvline(lcl, linestyle="--", label="LCL")
    ax2.set_xlabel("Sample Mean")
    ax2.set_ylabel("Frequency")
    ax2.legend()
    st.pyplot(fig2)

st.subheader("X-bar Control Chart")

fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.plot(sample_means, marker="o", markersize=3, linestyle="-")
ax3.axhline(center_line, linestyle="--", label="Center Line")
ax3.axhline(ucl, linestyle="--", label="UCL")
ax3.axhline(lcl, linestyle="--", label="LCL")

if num_out_of_control > 0:
    ax3.scatter(out_of_control_points, sample_means[out_of_control_points], s=50, label="Out of Control")

ax3.set_xlabel("Sample Number")
ax3.set_ylabel("Sample Mean")
ax3.set_title("Process Monitoring Using Sample Means")
ax3.legend()
st.pyplot(fig3)

st.subheader("Simulation Results")

col3, col4, col5, col6 = st.columns(4)

with col3:
    st.metric("Center Line", round(center_line, 2))

with col4:
    st.metric("UCL", round(ucl, 2))

with col5:
    st.metric("LCL", round(lcl, 2))

with col6:
    st.metric("Out-of-Control Points", num_out_of_control)

st.subheader("Process Status")

if num_out_of_control == 0:
    st.success("The process appears to be in control based on the 3-sigma control limits.")
else:
    st.error("The process may be out of control because one or more sample means are outside the control limits.")

st.write("""
### Quality Engineering Explanation

This dashboard simulates a process and collects repeated samples from it.
The sample means are plotted on an X-bar control chart.

The Central Limit Theorem explains why sample means tend to follow an approximately
normal distribution as the sample size increases. This is useful in Quality Engineering
because control charts often rely on sample means to monitor process stability.

If sample means fall outside the upper or lower control limits, the process may have
special-cause variation and should be investigated.
""")
