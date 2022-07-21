import pandas as pd
import xgboost as xgb
import plotly.graph_objs as go

from prophet import Prophet
from prophet.plot import plot_plotly


def make_forecast_prophet(df, days_to_predict):
    """
    Make a forecast using Prophet.
    """
    model = Prophet(seasonality_mode="multiplicative")
    model.add_country_holidays(country_name="US")
    model.fit(df.rename(columns={"datetime": "ds", "traffic": "y"}))
    future = model.make_future_dataframe(periods=days_to_predict)
    forecast = model.predict(future)

    fig = plot_plotly(model, forecast)
    fig.update_layout(yaxis_title="Traffic", xaxis_title="Datetime")

    return fig, future, forecast


def _create_features_xgboost(df):
    """
    Create time series features based on time series index.
    """
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    df["dayofweek"] = df.index.dayofweek
    df["dayofyear"] = df.index.dayofyear
    df["week"] = df.index.week
    df["month"] = df.index.month
    df["year"] = df.index.year
    features = ["dayofweek", "dayofyear", "week", "month", "year"]

    return df, features


def _plotly_layout(show_legend=False):
    """
    Create a Plotly layout.
    """
    return dict(
        showlegend=show_legend,
        width=900,
        height=600,
        yaxis=dict(title="Traffic"),
        xaxis=dict(
            title="Datetime",
            type="date",
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=7, label="1w", step="day", stepmode="backward"),
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
        ),
    )


def _plot_plotly_xgboost(train, test):
    """
    Create a Plotly figure using XGBoost results.
    """
    data = []

    # Add Actual
    data.append(
        go.Scatter(
            name="Actual",
            x=train.index,
            y=train.traffic,
            marker=dict(color="black", size=4),
            mode="markers",
        )
    )

    # Add prediction
    data.append(
        go.Scatter(
            name="Predicted",
            x=train.index,
            y=train.pred,
            mode="lines",
            line=dict(color="#0072B2", width=2),
            fillcolor="rgba(0, 114, 178, 0.2)",
            fill="none",
        )
    )

    data.append(
        go.Scatter(
            name="Predicted",
            x=test.index,
            y=test.pred,
            mode="lines",
            line=dict(color="#0072B2", width=2),
            fillcolor="rgba(0, 114, 178, 0.2)",
            fill="none",
        )
    )

    fig = go.Figure(data=data, layout=_plotly_layout())

    return fig


def make_forecast_xgboost(df, future):
    """
    Make a forecast using XGBoost.
    """
    train, features = _create_features_xgboost(df.set_index("datetime"))
    test, features = _create_features_xgboost(future.set_index("ds"))

    X_train, y_train = train[features], train["traffic"]
    X_test = test[features]

    reg = xgb.XGBRegressor(n_estimators=500, learning_rate=0.01)
    reg.fit(X_train, y_train, eval_set=[(X_train, y_train)], verbose=100)

    train["pred"] = reg.predict(X_train)
    test["pred"] = reg.predict(X_test)

    return _plot_plotly_xgboost(train, test), test


def results_comparison(df, prophet_pred, xgboost_pred, days_to_predict):
    """
    Compare the results of Prophet and XGBoost.
    """
    x = prophet_pred.ds.values[-days_to_predict * 2 :]
    y_prophet = prophet_pred.yhat.values[-days_to_predict * 2 :]
    y_xgboost = xgboost_pred.pred.values[-days_to_predict * 2 :]

    data = []

    data.append(
        go.Scatter(
            name="Actual",
            x=df.datetime.values[-days_to_predict:],
            y=df.traffic.values[-days_to_predict:],
            marker=dict(color="black", size=4),
            mode="markers",
        )
    )

    data.append(
        go.Scatter(
            name="Prophet",
            x=x,
            y=y_prophet,
            mode="lines",
            line=dict(color="#0072B2", width=2),
        )
    )

    data.append(
        go.Scatter(
            name="XGBoost",
            x=x,
            y=y_xgboost,
            mode="lines",
            line=dict(color="orange", width=2),
        )
    )

    fig = go.Figure(data=data, layout=_plotly_layout(show_legend=True))

    fig.add_vline(
        x=pd.to_datetime(x[int(len(x) / 2)]), line_dash="dash", line_color="green"
    )

    return fig


def make_forecast(df, days_to_predict):
    """
    Make a forecast using Prophet and XGBoost.
    """
    prophet_fig, future, prophet_pred = make_forecast_prophet(
        df.copy(), days_to_predict
    )
    xgboost_fig, xgboost_pred = make_forecast_xgboost(df.copy(), future)
    comparison_fig = results_comparison(df, prophet_pred, xgboost_pred, days_to_predict)

    return prophet_fig, xgboost_fig, comparison_fig
