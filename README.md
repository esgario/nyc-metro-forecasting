# NYC Metro Dataset

Exploratory Data Analysis and Forecasting of the NYC Metro Dataset

## Notebooks

[Exploratory Data Analysis](https://nbviewer.org/github/esgario/nyc-metro-forecasting/blob/v0/1_exploratory_data_analysis.ipynb)

[Forecasting](https://nbviewer.org/github/esgario/nyc-metro-forecasting/blob/v0/2_forecasting.ipynb)

## Download Dataset

You can download the dataset from the following link:

[https://drive.google.com/file/d/1CuE9I4x0_Agm2BMkWfnSSbiGm0-pTDuc/view?usp=sharing](https://drive.google.com/file/d/1CuE9I4x0_Agm2BMkWfnSSbiGm0-pTDuc/view?usp=sharing)

After downloading the dataset, you must unzip it and move all the csv files to the `dataset` folder. After that, you will have the files organized in the following way:

```
nyc-metro-forecasting/
    dataset/
        2010.csv
        2011.csv
        2012.csv
        2013.csv
        2014.csv
        2015.csv
        2016.csv
        2017.csv
    ...
```

## Installing Requirements

Activate your virtual environment and install the requirements by running the following commands:

```bash
pip install -U pip wheel setuptools
pip install -r requirements.txt
```

## Web APP

I've created a simple web app to visualize and forecast the NYC Metro dataset. You can access it by running the following command:

```bash
streamlit run app/run.py
```