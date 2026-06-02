import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import os
from analytics.historical_analysis import (load_historical_reports,calculate_waste_trend)
from analytics.cost_explorer import get_service_costs

# PAGE CONFIG
st.set_page_config(page_title="Cloud Cost Optimizer",layout="wide")

# LOAD HISTORICAL DATA
historical_df = load_historical_reports()
total_waste = historical_df[
    "EstimatedWasteUSD"
].sum()
#Adding Filters to instances
instance_filter = st.selectbox(
    "Filter by Instance Type",
    ["All"]
    + list(
        historical_df[
            "InstanceType"
        ].unique()
    )
)
filtered_df = historical_df
idle_df = filtered_df[
    filtered_df["CPUIdle"] == True
]
st.subheader("Idle Instances")
st.dataframe(
    idle_df,
    use_container_width=True
)

if instance_filter != "All":
    filtered_df = historical_df[
        historical_df["InstanceType"]
        == instance_filter
    ]
# SIDEBAR NAVIGATION
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select View",
    ["Overview","Historical Analytics","Billing Analytics","EBS Analysis"])

# OVERVIEW PAGE
if page == "Overview":
    st.title("Cloud Cost Optimizer Dashboard")
    st.write("AWS Cloud Analytics Platform")
    # ---------------- KPIs ----------------
    total_waste = filtered_df[
    "EstimatedWasteUSD"].sum()

    idle_instances = filtered_df[
    filtered_df["CPUIdle"] == True].shape[0]
    col1, col2, col3 = st.columns(3)
    BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
    )

    REPORTS_DIR = os.path.join(
    BASE_DIR,
    "reports_output"
    )
    ebs_files = glob.glob(
        os.path.join(
        REPORTS_DIR,
        "ebs_report_*.csv"
    )
    )
    if ebs_files:
        latest_ebs_file = max(
        ebs_files,
        key=os.path.getctime
    )
        try:
            ebs_df = pd.read_csv(
            latest_ebs_file
        )
        except pd.errors.EmptyDataError:
            ebs_df = pd.DataFrame()

    else:
        ebs_df = pd.DataFrame()
    with col1:
         st.metric("Total Historical Waste",f"${total_waste}")

    with col2:
        st.metric("Idle Instances",idle_instances)
        
    with col3:
        st.metric("Unused EBS Volumes",len(ebs_df))
    # ---------------- Historical Trend ----------------
    st.subheader("Historical Waste Trend")
    trend = calculate_waste_trend(filtered_df)
    fig = px.line(
    x=trend.index,
    y=trend.values,
    labels={
        "x": "Date",
        "y": "Waste ($)"
    },
    title="Historical Waste Trend"
    )
    st.plotly_chart(
    fig,
    use_container_width=True
    )

    # ---------------- Service Costs ----------------
    st.subheader("AWS Service Costs")
    service_costs = get_service_costs()
    service_df = pd.DataFrame(service_costs)

    if not service_df.empty:
        fig = px.bar(service_df,x="Service",y="CostUSD",title="AWS Service Billing",height=500)
        st.plotly_chart(fig,use_container_width=True)
    else:
        st.warning("No billing data available")

# HISTORICAL ANALYTICS PAGE
elif page == "Historical Analytics":
    st.title("Historical Analytics")
    st.subheader("Historical EC2 Reports")
    st.dataframe(filtered_df,use_container_width=True)

    trend = calculate_waste_trend(filtered_df)
    st.subheader("Historical Waste Trend")
    fig = px.line(
    x=trend.index,
    y=trend.values,
    labels={
        "x": "Date",
        "y": "Waste ($)"
    },
    title="Historical Waste Trend"
    )
    st.plotly_chart(
    fig,
    use_container_width=True
    )
    latest_report = filtered_df.tail(1)

    st.subheader("Latest Cloud Snapshot")

    st.dataframe(
    latest_report,
    use_container_width=True
)
# BILLING ANALYTICS PAGE
elif page == "Billing Analytics":
    st.title("Billing Analytics")
    service_costs = get_service_costs()
    service_df = pd.DataFrame(service_costs)
    st.subheader("AWS Service Billing Data")
    st.dataframe(
        service_df,
        use_container_width=True
    )

    if not service_df.empty:
        fig = px.bar(
            service_df,
            x="Service",
            y="CostUSD",
            title="AWS Service Costs",
            height=600
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# EBS ANALYSIS PAGE
elif page == "EBS Analysis":
    st.title("EBS Waste Analysis")
    try:
        ebs_files = glob.glob(
            "reports_output/ebs_report_*.csv"
        )
        latest_ebs_file = max(
            ebs_files,
            key=os.path.getctime
        )
        ebs_df = pd.read_csv(
            latest_ebs_file
        )
        st.subheader("Unused EBS Volumes")
        st.dataframe(
            ebs_df,
            use_container_width=True
        )
        if not ebs_df.empty:
            fig = px.bar(
                ebs_df,
                x="VolumeId",
                y="EstimatedWasteUSD",
                title="Unused EBS Volume Waste",
                height=500
            )
            st.plotly_chart(
                fig,
                use_container_width=True
            )
        else:
            st.warning(
                "No unused EBS volumes detected"
            )
    except Exception as e:
        st.error(
            f"EBS report could not be loaded: {e}"
        )

#Right SIzing Page
elif page == "Rightsizing":
    st.title(
        "EC2 Rightsizing Recommendations"
    )

    latest_df = historical_df

    recommendations = latest_df[
        latest_df["Recommendation"] !=
        "Instance appropriately sized"
    ]

    st.dataframe(
        recommendations,
        use_container_width=True
    )
    fig = px.bar(

    recommendations,

    x="InstanceId",

    y="PotentialSavingsUSD",

    color="Recommendation",

    title="Potential Rightsizing Savings"
)

    st.plotly_chart(
    fig,
    use_container_width=True,
    key="rightsizing_savings_chart"
)
#Final Summary of aws credentials
#st.write(historical_df.columns.tolist())
rightsized_count = (
    historical_df[
        historical_df["PotentialSavingsUSD"] > 0
    ].shape[0]
)
st.metric(
    "Rightsizing Opportunities",
    rightsized_count
)
csv = historical_df.to_csv(index=False)
# Adding download button to reports page
st.download_button(

    label="Download Historical Report",

    data=csv,

    file_name="historical_report.csv",

    mime="text/csv"
)

#add pie chart to view idle vs active instances
ec2_files = glob.glob(
    "reports_output/ec2_report_*.csv"
)

latest_ec2_file = max(
    ec2_files,
    key=os.path.getctime
)

latest_df = pd.read_csv(
    latest_ec2_file
)
idle_count = latest_df[
    latest_df["CPUIdle"] == True
].shape[0]
active_count = latest_df[
    latest_df["CPUIdle"] == False
].shape[0]
pie_df = pd.DataFrame({
    "Status": [
        "Idle",
        "Active"
    ],
    "Count": [
        idle_count,
        active_count
    ]
})
fig = px.pie(
    pie_df,
    names="Status",
    values="Count",
    title="Current EC2 Instance Status"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="ec2_status_pie"
)
from analytics.cost_explorer import get_total_monthly_cost
monthly_cost = get_total_monthly_cost()

if monthly_cost == 0:
    st.metric(
        "AWS Monthly Cost",
        "Covered by Credits"
    )
else:
    st.metric(
        "AWS Monthly Cost",
        f"${monthly_cost}"
    )
st.metric(
    "Potential Monthly Savings",
    f"${total_waste}"
)
# Size recommendation
total_savings = historical_df[
    "PotentialSavingsUSD"
].sum()
st.metric(
    "Rightsizing Savings",
    f"${total_savings}"
)