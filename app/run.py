import os
import pandas as pd
import streamlit as st

from forecast import make_forecast


# Helpers
# ----------------------------------------------------------------------------
@st.cache
def load_data(data_dir="./dataset"):
    df_st = pd.read_parquet(os.path.join(data_dir, "daily_traffic_by_station.parquet"))
    df_ln = pd.read_parquet(os.path.join(data_dir, "daily_traffic_by_line.parquet"))
    df_tot = df_st.groupby("datetime").traffic.sum().reset_index()
    return df_st, df_ln, df_tot


# Build APP Page
# ----------------------------------------------------------------------------

# <<< Header >>>
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# <<< Body >>>
with st.sidebar:
    st.write(
        """
    # NYC Metro Forecast
    Simple app that allows us to do forecasting for different time series of NYC metro dataset.
    """
    )
    days = 365
    submitted = False
    df_st, df_ln, df = load_data()

    with st.form("my_form"):
        
        # <selectbox>
        dataset = st.selectbox("Forecasting by", ("Total traffic", "Station", "Line name"))

        # <selectbox>
        if dataset == "Station":
            option = st.selectbox("Select a station", df_st.station.unique())
            df = df_st.loc[df_st.station == option]

        elif dataset == "Line name":
            option = st.selectbox("Select a line", df_ln.linename.unique())
            df = df_ln.loc[df_ln.linename == option]

        # <selectbox>
        train_dt_interval = st.selectbox(
            "Training dataset", ("2015-2017", "2013-2017", "2010-2017 (All Data)")
        )
        show_warning = True

        if train_dt_interval == "2015-2017":
            df = df.loc[df.datetime >= "2015-01-01"]
            show_warning = False

        elif train_dt_interval == "2013-2017":
            df = df.loc[df.datetime >= "2013-01-01"]

        if show_warning:
            st.warning("obs: large datasets can take a long time to train.")

        # <selectbox>
        days = int(st.selectbox("Days to predict", ("30", "90", "180", "365"), index=3))

        # <selectbox>
        methods = st.multiselect("Methods", ["Prophet", "XGBoost"], ["Prophet", "XGBoost"])

        # <submit>
        submitted = st.form_submit_button("Run")

if submitted:
    with st.spinner(text="Forecasting..."):
        prophet_fig, xgboost_fig, comparison_fig = make_forecast(df, days)

        if "Prophet" in methods:
            st.write("## Prophet results")
            st.plotly_chart(prophet_fig, use_container_width=True)

        if "XGBoost" in methods:
            st.write("## XGBoost results")
            st.plotly_chart(xgboost_fig, use_container_width=True)

        if "Prophet" in methods and "XGBoost" in methods:
            st.write("## Comparison")
            st.plotly_chart(comparison_fig, use_container_width=True)

else:
    st.write("Please select a dataset and click on Run.")
