# Snowflake Account Usage Dashboard
A comprehnsive Streamlit application for monitoring and analyzing your Snowflake account usage across multiple dimensions.

![image](https://github.com/user-attachments/assets/ade074c1-89c1-4819-b95d-0c15b1091e74)

![image](https://github.com/user-attachments/assets/4afe2575-43be-4a70-ae21-968b3d760fa1)

![image](https://github.com/user-attachments/assets/d796fd1e-605a-4831-8c44-ef2a6d0ecfe4)

![image](https://github.com/user-attachments/assets/2ba8881b-dcdb-43b4-9d6c-6ac675966e51)

![image](https://github.com/user-attachments/assets/0db0a285-71ef-4a94-810e-6bb9779ccf21)

# Overview
This Snowflake Account Usage Dashboard provides a detailed view of your account's consumption, user activity, storage metrics, and performance statistics. The application leverages Snowflake's account_usage views to deliver actionable insights through an interactive Streamlit interface.

# Features
The dashboard is organized into four main tabs:

# 1. Consumption Dashboard

1. Track credit usage across different service types
2. Visualize daily credit consumption trends
3. Monitor warehouse-specific credit usage
4. Analyze cloud services utilization by query type
5. Review monthly credit billing history

# 2. Users Dashboard

1. View total, new, and dropped user metrics
2. Analyze failed login attempts and their causes
3. Explore client types used to access Snowflake
4. Compare successful vs. failed logins by client

# 3. Storage Dashboard

1. Monitor total storage consumption by type (TimeTravel, Stage, Failsafe)
2. Track storage trends over time
3. Analyze database-specific storage patterns
4. Identify short-lived tables that may impact billing
5. Visualize row loading patterns over time

# 4. Performance Dashboard

1. Track query execution metrics (success vs. failure)
2. Analyze query execution, compilation, and queuing times
3. Compare warehouse performance
4. Identify long-running queries
5. Monitor role-based query patterns
6. Review execution times by query type and user

# Setup Requirements

1. Python 3.8 or higher
2. Snowflake account with access to account_usage schema
3. Required Python packages:

streamlit
pandas
numpy
plotly
snowflake-snowpark-python

# Date Filtering
The dashboard allows filtering data by various timeframes:

Yesterday
Last 7 Days
Last Month
Last 3 Months
Last 6 Months
Last Year
All Time
Custom Date Range

# Acknowledgements
This dashboard utilizes Snowflake's account_usage views and the Streamlit framework to provide interactive data visualization.
