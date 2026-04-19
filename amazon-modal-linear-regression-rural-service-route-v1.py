import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

st.title("Amazon Warehouse Productivity Model")
st.write("Predicting Effective Throughput (April 5–12 data)")

# ============================
# Load and combine the real data from your images
# ============================

# Stow / Overall Defects Data
stow_data = {
    'User': ['narossoh', 'iqrayuss', 'uiyps', 'mnimhas', 'hersmary', 'mtiband r', 'danijac', 
             'nkaibrah', 'gpliegom', 'matstrak', 'hasnsai', 'elizev', 'pmhusse', 'stajenni', 
             'abdiosmg', 'jnoonoor', 'arrizola'],
    'Total_Defects_stow': [164, 130, 117, 94, 45, 37, 22, 17, 15, 13, 12, 12, 9, 7, 4, 3, 3],
    'Opportunities_stow': [1068, 758, 330, 668, 246, 445, 168, 518, 580, 594, 416, 204, 308, 127, 214, 63, 57],
    'PC99_to_DropZone': [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    'Sips_Over_And_Short': [19, 37, 7, 7, 9, 5, 1, 1, 1, 1, 1, 1, 2, 4, 1, 2, 0],
    'Scan_Out_Of_Sequence': [79, 58, 58, 32, 9, 19, 11, 8, 9, 7, 6, 3, 5, 0, 3, 0, 0],
    'Bin_Collision': [65, 34, 51, 54, 27, 13, 10, 8, 5, 5, 4, 7, 1, 3, 0, 1, 2]
}

df_stow = pd.DataFrame(stow_data)

# Pick Report Data
pick_data = {
    'User': ['narossoh', 'stajenni', 'danijac', 'arrizola', 'hasnsai', 'uiyps', 'jnoonoor', 
             'gpliegom', 'mtiband r', 'elizev', 'hersmary', 'mnimhas', 'iqrayuss', 'nkaibrah', 
             'matstrak', 'abdiosmg', 'musaom'],
    'Total_Defects_pick': [57, 14, 13, 13, 8, 8, 7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 2],
    'Opportunities_pick': [746, 804, 169, 614, 214, 208, 110, 362, 68, 176, 69, 97, 37, 255, 186, 44, 55],
    'Wrong_Asi': [57, 14, 13, 13, 8, 8, 7, 7, 5, 6, 5, 5, 4, 4, 3, 3, 2]
}

df_pick = pd.DataFrame(pick_data)

# Merge both reports on User
df = pd.merge(df_stow, df_pick, on='User', how='inner')

# Create target and features
df['Total_Defects'] = df['Total_Defects_stow'] + df['Total_Defects_pick']
df['Total_Opportunities'] = df['Opportunities_stow'] + df['Opportunities_pick']
df['Effective_Throughput'] = df['Total_Opportunities'] - df['Total_Defects']   # Proxy for productivity

# Features for the model
features = ['Opportunities_stow', 'Opportunities_pick', 'Scan_Out_Of_Sequence', 
            'Bin_Collision', 'Sips_Over_And_Short', 'PC99_to_DropZone']

X = df[features]
y = df['Effective_Throughput']

# Train Linear Regression
model = LinearRegression()
model.fit(X, y)

# ============================
# Streamlit UI
# ============================

st.sidebar.header("Adjust Input Values (Simulate Shift)")

input_opp_stow = st.sidebar.slider("Opportunities (Stow)", 50, 1200, 500)
input_opp_pick = st.sidebar.slider("Opportunities (Pick)", 50, 900, 300)
input_scan_seq = st.sidebar.slider("Scan Out of Sequence", 0, 100, 20)
input_bin_coll = st.sidebar.slider("Bin Collision", 0, 80, 15)
input_sips = st.sidebar.slider("Sips Over/Short", 0, 50, 10)
input_pc99 = st.sidebar.slider("PC99 to DropZone", 0, 5, 1)

# Prediction
input_data = np.array([[input_opp_stow, input_opp_pick, input_scan_seq, 
                        input_bin_coll, input_sips, input_pc99]])

prediction = model.predict(input_data)[0]

st.subheader("Prediction")
st.metric("Estimated Effective Throughput", f"{prediction:.1f}")

st.write("**Interpretation**: Higher value = better productivity (more volume with fewer defects).")

# Show model coefficients
st.subheader("Model Coefficients")
coef_df = pd.DataFrame({
    "Feature": features,
    "Coefficient": model.coef_
}).round(4)
st.dataframe(coef_df)

# Model performance
r2 = model.score(X, y)
st.write(f"**R² on training data**: {r2:.3f}")

# Preview of the real dataset used
st.subheader("Sample Training Data (Combined Reports)")
st.dataframe(df[['User', 'Total_Opportunities', 'Total_Defects', 'Effective_Throughput']].head(10))

st.caption("Model trained on real Amazon shift data from April 5–12. "
           "Coefficients show the estimated impact of each error type on throughput.")
