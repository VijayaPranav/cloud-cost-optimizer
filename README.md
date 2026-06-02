- Build Lambda package before deployment.

# Cloud Cost Optimizer
AWS-based cloud cost optimization platform that identifies:
- Idle EC2 instances
- Unused EBS volumes
- Estimated monthly waste
- Rightsizing opportunities
- Potential savings

## Features

- EC2 idle detection using CloudWatch metrics
- EBS waste analysis
- AWS Cost Explorer integration
- Historical trend analysis
- Streamlit dashboard
- S3 report storage
- Lambda + EventBridge automation

## Tech Stack

- Python
- AWS EC2
- AWS CloudWatch
- AWS Cost Explorer
- AWS Lambda
- AWS EventBridge
- AWS S3
- Streamlit
- Pandas
- Plotly

## Run Locally

```bash
pip install -r requirements.txt
python main.py
streamlit run dashboard.py