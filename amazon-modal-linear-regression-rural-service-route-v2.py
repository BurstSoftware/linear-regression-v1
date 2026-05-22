import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

st.title("Amazon Warehouse Productivity Model")

st.write("Predict total packages processed based on workforce allocation.")

# Generate synthetic dataset
np.random.seed(42)

n_samples = 100

picking = np.random.randint(5, 50, n_samples)
shipping = np.random.randint(5, 50, n_samples)
idle = np.random.randint(0, 20, n_samples)

# Assume picking contributes more than shipping, idle contributes nothing
packages = (picking * 10) + (shipping * 7) + (idle * 0) + np.random.normal(0, 10, n_samples)

data = pd.DataFrame({
    "Picking": picking,
    "Shipping": shipping,
    "Idle": idle,
    "Packages": packages
})

# Train model
X = data[["Picking", "Shipping", "Idle"]]
y = data["Packages"]

model = LinearRegression()
model.fit(X, y)

# Sidebar inputs
st.sidebar.header("Adjust Workforce")

input_picking = st.sidebar.slider("Picking Associates", 0, 100, 20)
input_shipping = st.sidebar.slider("Shipping Associates", 0, 100, 20)
input_idle = st.sidebar.slider("Idle Associates", 0, 50, 5)

# Prediction
input_data = np.array([[input_picking, input_shipping, input_idle]])
prediction = model.predict(input_data)[0]

# Output
st.subheader("Prediction")
st.write(f"Estimated Packages Processed: **{prediction:.2f}**")

# Show coefficients
st.subheader("Model Coefficients")
coef_df = pd.DataFrame({
    "Feature": ["Picking", "Shipping", "Idle"],
    "Coefficient": model.coef_
})
st.write(coef_df)

# Data preview
st.subheader("Sample Training Data")
st.write(data.head())
