import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
def load_historical_reports():

    files = glob.glob("reports_output/ec2_report_*.csv")

    all_reports = []

    for file in files:

        try:
            df = pd.read_csv(file)

            filename = os.path.basename(file)

            report_date = filename.replace(
                "ec2_report_",
                ""
            ).replace(
                ".csv",
                ""
            )

            df["ReportDate"] = report_date

            all_reports.append(df)

        except pd.errors.EmptyDataError:
            print(f"Skipping bad file: {file}")
            continue

    if all_reports:
        return pd.concat(
            all_reports,
            ignore_index=True
        )

    return pd.DataFrame()
def calculate_waste_trend(df):

    trend = df.groupby(
        "ReportDate"
    )["EstimatedWasteUSD"].sum()

    return trend
#graph for historical cost wastage
def plot_waste_trend(trend):
    plt.figure(figsize=(12,5))
    trend.plot(kind='line',marker='o')
    plt.xlabel("Timestamp")
    plt.ylabel("Total Waste ($)")
    plt.title("Historical Cloud Waste Trend")
    plt.xticks(rotation=20)
    plt.grid(True)
    plt.tight_layout()
    plt.show()