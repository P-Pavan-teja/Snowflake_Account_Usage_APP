# Import Python Packages
import pandas as pd
import numpy as np
import streamlit as st
import datetime as dtt
import plotly.express as px
from snowflake.snowpark.context import get_active_session

#############################################
#     FORMATTING
#############################################


# Initialize session state at startup
def init_session_state():
    defaults = {
        'date_filter': "7 Days",
        'current_tab': "Consumption",
        'data_loaded': {},
        'start_date': dtt.datetime.now() - dtt.timedelta(days=7),
        'end_date': dtt.datetime.now()
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Page config (must be first Streamlit command)
st.set_page_config(
    layout="wide",
    page_title="Snowflake Usage Dashboard",
    page_icon="❄️"
)

# Initialize states
init_session_state()

# Apply custom CSS for better performance
st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 24px;
            font-weight: bold;
        }
        .reportview-container .main .block-container {
            max-width: 95%;
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Title and date filter section
st.title("Snowflake Account Usage App :snowflake:")
st.divider()

# Efficient date filtering
def get_date_range(filter_option):
    end_date = dtt.datetime.today() 
    date_ranges = {
        "Yesterday": (end_date - dtt.timedelta(days=1), end_date),
        "7 Days": (end_date - dtt.timedelta(days=7), end_date),
        "1 Month": (end_date - dtt.timedelta(days=30), end_date),
        "3 Months": (end_date - dtt.timedelta(days=90), end_date),
        "6 Months": (end_date - dtt.timedelta(days=180), end_date),
        "1 Year": (end_date - dtt.timedelta(days=365), end_date),
        "All Time": (dtt.datetime(2000, 1, 1).date(), end_date)
    }
    return date_ranges.get(filter_option, (None, None))

# Efficient date filter UI
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        date_filter = st.selectbox(
            "📅 Select Date Range",
            ["Yesterday", "7 Days", "1 Month", "3 Months", "6 Months", "1 Year", "All Time", "Custom Date Range"],
            key='date_filter'
        )
    
    if date_filter == "Custom Date Range":
        with col2:
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                start_date = st.date_input("Start Date", dtt.datetime.today() - dtt.timedelta(days=30))
            with sub_col2:
                end_date = st.date_input("End Date", dtt.datetime.today())
    else:
        start_date, end_date = get_date_range(date_filter)

            
#########################################################################################################################################################
#############################################
#     Get the current credentials
#############################################

session = get_active_session()

#############################################
#     cache data
#############################################

@st.cache_data
def run_quey(query):
    return session.sql(query).to_pandas()
                    
#############################################
#     Tab Creation
#############################################

Consumption_tab, Users_tab, Storage_tab, Performance_tab = st.tabs(["Consumption Dashboard | ","Users Dashboard | ", "Storage Dashboard | ","Performance Dashboard"])

##########################################################################################################################################################
##################################################     Consumption Dashboard   ###########################################################################
##########################################################################################################################################################

with Consumption_tab:

    st.header('Consumption Dashboard')
    st.divider()

    #############################################
    #     Cards at Top
    #############################################

    st.subheader('**Credits Usage**')

    #Credits Used
    credits_used_sql = f"select round(sum(credits_used),2) as total_credits from snowflake.account_usage.metering_history where start_time between '{start_date}' and '{end_date}'"
    pandas_credits_used_df = session.sql(credits_used_sql).to_pandas()
    #Final Value
    credits_used_tile = pandas_credits_used_df.iloc[0].values

    # Credits Used by Warehouse Metering
    credits_used_wh_sql = f"select coalesce(round(sum(credits_used),2),0) from snowflake.account_usage.metering_history where (start_time between '{start_date}' and '{end_date}') and service_type = 'WAREHOUSE_METERING'"
    pandas_credits_used_wh_df = session.sql(credits_used_wh_sql).to_pandas()
    #Final Value
    credits_used_wh_tile = pandas_credits_used_wh_df.iloc[0].values
    
    # Credits Used by Warehouse Metering
    credits_used_pipe_sql = f"select coalesce(round(sum(credits_used),2),0) from snowflake.account_usage.metering_history where (start_time between '{start_date}' and '{end_date}') and service_type = 'PIPE'"
    pandas_credits_used_pipe_df = session.sql(credits_used_pipe_sql).to_pandas()
    #Final Value
    credits_used_pipe_tile = pandas_credits_used_pipe_df.iloc[0].values
    
    # Credits Used by Warehouse Metering
    credits_used_tc_sql = f"select coalesce(round(sum(credits_used),2),0) from snowflake.account_usage.metering_history where (start_time between '{start_date}' and '{end_date}') and service_type = 'TRUST_CENTER'"
    pandas_credits_used_tc_df = session.sql(credits_used_tc_sql).to_pandas()
    #Final Value
    credits_used_tc_tile = pandas_credits_used_tc_df.iloc[0].values
    
    # Credits Used by Warehouse Metering
    credits_used_st_sql = f"select coalesce(round(sum(credits_used),2),0) from snowflake.account_usage.metering_history where (start_time between '{start_date}' and '{end_date}') and service_type = 'SERVERLESS_TASK'"
    pandas_credits_used_st_df = session.sql(credits_used_st_sql).to_pandas()
    #Final Value
    credits_used_st_tile = pandas_credits_used_st_df.iloc[0].values

    # Credits Used by Warehouse Metering
    credits_used_mv_sql = f"select coalesce(round(sum(credits_used),2),0) from snowflake.account_usage.metering_history where (start_time between '{start_date}' and '{end_date}') and service_type = 'MATERIALIZED_VIEW'"
    pandas_credits_used_mv_df = session.sql(credits_used_mv_sql).to_pandas()
    #Final Value
    credits_used_mv_tile = pandas_credits_used_mv_df.iloc[0].values
    
    #Column formatting and metrics of header 3 metrics
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Credits","{:,}".format(float(credits_used_tile))) 
    col2.metric("Warehouse Metering","{:,}".format(float(credits_used_wh_tile))) 
    col3.metric("PIPE","{:,}".format(float(credits_used_pipe_tile))) 
    col4.metric("Trust Center","{:,}".format(float(credits_used_tc_tile))) 
    col5.metric("Server less Task","{:,}".format(float(credits_used_st_tile))) 
    col6.metric("Materialized Views","{:,}".format(float(credits_used_mv_tile))) 


    #############################################
    #     Credit Usage (Bar Chart)
    #############################################
    
    #Credits Usage (Total)
    credits_used_sql = f"SELECT start_time::date as usage_date, ROUND(SUM(credits_used), 2) as Total_credits_used FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY WHERE  start_time::date between '{start_date}' and '{end_date}'  GROUP BY  start_time::date"
    pandas_credits_used_df = session.sql(credits_used_sql).to_pandas()
     
    #Chart
    fig_credits_used=px.bar(pandas_credits_used_df,x= 'USAGE_DATE',y='TOTAL_CREDITS_USED',color='TOTAL_CREDITS_USED',orientation='v',title="Credits Usage")
    fig_credits_used.update_traces(texttemplate = '%{y}',textfont = dict(size=14))
    fig_credits_used.update_layout(legend =dict(orientation='h',yanchor='bottom',y=1.02,xanchor='center',x=0.5))
    st.plotly_chart(fig_credits_used, use_container_width=True)
    
    #############################################
    #     Credits by Service Type (Bar Chart)
    #############################################
    
    #Credits Usage (Total)
    credits_used_type_sql = f"SELECT start_time::date as usage_date, ROUND(SUM(credits_used), 2) as Total_credits_used, service_type FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY WHERE  start_time::date between '{start_date}' and '{end_date}'  GROUP BY  start_time::date, service_type"
    pandas_credits_used_type_df = session.sql(credits_used_type_sql).to_pandas()
     
    #Chart
    fig_credits_used_type=px.bar(pandas_credits_used_type_df,x='USAGE_DATE',y='TOTAL_CREDITS_USED',color='SERVICE_TYPE',orientation='v',title="Credits Used by Service type")
    fig_credits_used_type.update_traces(texttemplate = '%{y}',textfont = dict(size=14))
    fig_credits_used_type.update_layout(legend =dict(orientation='h',yanchor='bottom',y=1.02,xanchor='center',x=0.5))
    
    st.plotly_chart(fig_credits_used_type, use_container_width=True)

    #############################################
    #     Credits by WareHouse (Bar Chart)
    #############################################
    
    #Credits Usage (Total)
    credits_used_warehouse_sql = f"select start_time::date as usage_date, sum(credits_used) as Total_credits_used, warehouse_name from snowflake.account_usage.warehouse_metering_history where start_time between '{start_date}' and '{end_date}' group by 1,3 order by 3,1"
    pandas_credits_used_warehouse_df = session.sql(credits_used_warehouse_sql).to_pandas()
     
    #Chart
    fig_credits_used_warehouse=px.bar(pandas_credits_used_warehouse_df,x='USAGE_DATE',y='TOTAL_CREDITS_USED',color='WAREHOUSE_NAME',orientation='v',title="Credits Used by Warehouse")
    st.plotly_chart(fig_credits_used_warehouse, use_container_width=True)

    #############################################
    #     GS Utilization by Query Type (Top 10)
    #############################################
    
    gs_utilization = f"select query_type, sum(credits_used_cloud_services) cs_credits, count(1) num_queries from snowflake.account_usage.query_history where true and start_time::date between '{start_date}' and '{end_date}' group by 1 order by 2 desc limit 10"
    gs_utilization_df = session.sql(gs_utilization).to_pandas()
    #st.write(gs_utilization_df)
    fig_gs_utilization=px.bar(gs_utilization_df,x='QUERY_TYPE',y='CS_CREDITS', orientation='v',title="Credit Utilization by Query Type (Top 10)")
    fig_gs_utilization.update_traces(marker_color='green')

    #############################################
    #     Top 10 Cloud Services by Warehouse                 
    #############################################
    
    compute_gs_by_warehouse = f"select warehouse_name, sum(credits_used_cloud_services) CREDITS_USED_CLOUD_SERVICES from snowflake.account_usage.warehouse_metering_history where true and start_time::date between '{start_date}' and '{end_date}'  group by 1 order by 2 desc limit 10"
    compute_gs_by_warehouse_df = session.sql(compute_gs_by_warehouse).to_pandas()
    #st.write(compute_gs_by_warehouse_df)
    fig_compute_gs_by_warehouse=px.bar(compute_gs_by_warehouse_df,x='WAREHOUSE_NAME',y='CREDITS_USED_CLOUD_SERVICES', orientation='v',title="Compute and Cloud Services by Warehouse", barmode="group")
    fig_compute_gs_by_warehouse.update_traces(marker_color='purple')
    
    #############################################
    #     Container 3: Cloud services
    #############################################
    
    container2 = st.container()
    
    with container2:
        plot1, plot2 = st.columns(2)
        with plot1:
            st.plotly_chart(fig_gs_utilization, use_container_width=True)
        with plot2:
            st.plotly_chart(fig_compute_gs_by_warehouse, use_container_width=True)


    ############################################
        # Credits Billed by Month
    ############################################

    st.info('The below chart is static and not modified by the date range filter', icon="ℹ️")
    
    credits_billed = f"select date_trunc('MONTH', usage_date) as Usage_Month, sum(CREDITS_BILLED) as CREDITS_BILLED  from snowflake.account_usage.metering_daily_history group by Usage_Month"
    credits_billed_df = session.sql(credits_billed).to_pandas()
    #st.write(credits_billed_df)
    fig_credits_billed=px.bar(credits_billed_df,x='USAGE_MONTH',y='CREDITS_BILLED',color='CREDITS_BILLED', orientation='v',title="Credits Billed by Month")
    fig_credits_billed.update_layout(showlegend=False)
    
    st.plotly_chart(fig_credits_billed, use_container_width=True)

    #############################################
    #     FOOTER
    #############################################    
    st.divider()

##########################################################################################################################################################
########################################################     Users Dashboard   ###########################################################################
##########################################################################################################################################################

with Users_tab:

    st.header('Users Dashboard')
    st.divider()


    #############################################
    #     Cards at Top
    #############################################

    # Total Users
    total_users_sql = f"select count(distinct name) as total_users from snowflake.account_usage.users where deleted_on is null"
    total_users_df = session.sql(total_users_sql)
    pandas_total_users_df = total_users_df.to_pandas()
    #Final Value
    total_users_tile = pandas_total_users_df.iloc[0].values
    #st.metric("Total Users",total_users_tile)

    # New Users Count
    new_user_cnt_sql = f"select count(distinct name) as new_user_cnt from snowflake.account_usage.users where created_on  between '{start_date}'::date and '{end_date}'::date and deleted_on is null"
    new_user_cnt_df = session.sql(new_user_cnt_sql)
    pandas_new_user_cnt_df = new_user_cnt_df.to_pandas()
    #Final Value
    new_user_cnt_tile = pandas_new_user_cnt_df.iloc[0].values
    #st.metric("New Users Count",new_user_cnt_tile)
    
    # New Users Count
    dropped_cnt_sql = f"select count(distinct name) as dropped_cnt from snowflake.account_usage.users where created_on  between '{start_date}'::date and '{end_date}'::date and deleted_on is not null"
    dropped_cnt_df = session.sql(dropped_cnt_sql)
    pandas_dropped_cnt_df = dropped_cnt_df.to_pandas()
    #Final Value
    dropped_cnt_tile = pandas_dropped_cnt_df.iloc[0].values
    #st.metric("New Users Count",dropped_cnt_tile)

    
    #Column formatting 
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users",total_users_tile)
    col2.metric("New Users",new_user_cnt_tile)
    col3.metric("Dropped Users",dropped_cnt_tile)

    #############################################
    #  Failed Login Attempts
    #############################################
    
    #Failed Login Attempts
    Failed_Login_Attempts_sql = f"""
                        Select count(*) as Count, ERROR_MESSAGE from snowflake.account_usage.login_history where error_code is not null and event_timestamp between '{start_date}'::date and '{end_date}'::date
                        group by error_message
                        order by count asc
                   
                                """
    pandas_Failed_Login_Attempts_df = session.sql(Failed_Login_Attempts_sql).to_pandas()
     
    #Chart,
    fig_Failed_Login_Attempts=px.bar(pandas_Failed_Login_Attempts_df,x= 'COUNT',y='ERROR_MESSAGE' ,orientation='h',title="Failed Login Attempts")
    st.plotly_chart(fig_Failed_Login_Attempts, use_container_width=True)

    #############################################
    #  Client Types
    #############################################
    
    #Failed Login Attempts
    client_types_sql = f"""
                        Select count(*) Count, REPORTED_CLIENT_TYPE  from snowflake.account_usage.login_history where event_timestamp between '{start_date}'::date and '{end_date}'::date
                        group by REPORTED_CLIENT_TYPE
                        order by count asc
                   
                                """
    pandas_client_types_df = session.sql(client_types_sql).to_pandas()
     
    #Chart,
    fig_client_types=px.bar(pandas_client_types_df,x= 'COUNT',y='REPORTED_CLIENT_TYPE' ,orientation='h',title="Client Types")
    st.plotly_chart(fig_client_types, use_container_width=True)

    #############################################
    #     Logins by Client               
    #############################################
    
    scc_logins_client = "select reported_client_type as Client, sum(iff(is_success = 'NO', 1, 0)) as Failed, count(*) as Success, from snowflake.account_usage.login_history group by 1 order by SUCCESS asc"
    scc_logins_client_df = session.sql(scc_logins_client).to_pandas()
    
    fig_scc_logins_client=px.bar(scc_logins_client_df,x='SUCCESS',y='CLIENT', orientation='h',title="Successfull Logins by Client")
    #st.plotly_chart(fig_scc_logins_client, use_container_width=True)

    #############################################
    #     Logins by Client               
    #############################################
    
    fail_logins_client = "select reported_client_type as Client, sum(iff(is_success = 'NO', 1, 0)) as Failed, count(*) as Success, from snowflake.account_usage.login_history group by 1 order by FAILED asc"
    fail_logins_client_df = session.sql(fail_logins_client).to_pandas()
    
    fig_fail_logins_client=px.bar(fail_logins_client_df,x='FAILED',y='CLIENT', orientation='h',title="Failed Logins by Client")
    #st.plotly_chart(fig_fail_logins_client, use_container_width=True)

    #############################################

    #Column formatting 
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_scc_logins_client, use_container_width=True)
    col2.plotly_chart(fig_fail_logins_client, use_container_width=True)

    #############################################
    #     FOOTER
    #############################################    
    st.divider()

##########################################################################################################################################################
########################################################   Storage Dashboard   ###########################################################################
##########################################################################################################################################################

with Storage_tab:

    st.header('Storage Dashboard')
    st.divider()

    #############################################
    #     Cards at Top
    #############################################

    # totlal Storage in TB
    current_storage_tb_sql = f"select round(sum(storage_bytes + stage_bytes + failsafe_bytes) / power(1024, 4),2) as billable_TB from snowflake.account_usage.storage_usage"
    current_storage_tb_df = session.sql(current_storage_tb_sql)
    pandas_current_storage_tb_df = current_storage_tb_df.to_pandas()
    #Final Value
    current_storage_tb_tile = pandas_current_storage_tb_df.iloc[0].values
    #st.metric("Current Storage (TB)",current_storage_tb_tile)

    # TimeTravel Storage in TB
    current_tt_storage_tb_sql = f"select round(sum( storage_bytes) / power(1024, 4),2) as billable_TB from snowflake.account_usage.storage_usage"
    current_tt_storage_tb_df = session.sql(current_tt_storage_tb_sql)
    pandas_current_tt_storage_tb_df = current_tt_storage_tb_df.to_pandas()
    #Final Value
    current_tt_storage_tb_tile = pandas_current_tt_storage_tb_df.iloc[0].values
    #st.metric("Current Storage (TB)",current_tt_storage_tb_tile)
    
    # Satge Storage in TB
    current_stg_storage_tb_sql = f"select round(sum( stage_bytes ) / power(1024, 4),2) as billable_TB from snowflake.account_usage.storage_usage"
    current_stg_storage_tb_df = session.sql(current_stg_storage_tb_sql)
    pandas_current_stg_storage_tb_df = current_stg_storage_tb_df.to_pandas()
    #Final Value
    current_stg_storage_tb_tile = pandas_current_stg_storage_tb_df.iloc[0].values
    #st.metric("Current Storage (TB)",current_stg_storage_tb_tile)

    # Failsafe Storage in TB
    current_fs_storage_tb_sql = f"select round(sum(failsafe_bytes) / power(1024, 4),2) as billable_TB from snowflake.account_usage.storage_usage"
    current_fs_storage_tb_df = session.sql(current_fs_storage_tb_sql)
    pandas_current_fs_storage_tb_df = current_fs_storage_tb_df.to_pandas()
    #Final Value
    current_fs_storage_tb_tile = pandas_current_fs_storage_tb_df.iloc[0].values
    #st.metric("Current Storage (TB)",current_fs_storage_tb_tile)
    
    #Column formatting and metrics of header 3 metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Storage (TB)",current_storage_tb_tile)
    col2.metric("TimeTravel Storage (TB)",current_tt_storage_tb_tile)
    col3.metric("Stage Storage (TB)",current_stg_storage_tb_tile)
    col4.metric("Fail Safe Storage (TB)",current_fs_storage_tb_tile)
    

    #############################################
    #     Data Storage used Overtime                
    #############################################
    st.divider()

    st.info('The below chart is static and non modified by the date range filter', icon="ℹ️")
    
    
    storage_overtime = "select date_trunc(month, usage_date) as usage_month, avg(storage_bytes + stage_bytes + failsafe_bytes) / power(1024, 3) as billable_gb, avg(storage_bytes) / power(1024, 3) as Storage_gB, avg(stage_bytes) / power(1024, 3) as Stage_gB, avg(failsafe_bytes) / power(1024, 3) as Failsafe_gB from snowflake.account_usage.storage_usage group by 1 order by 1"
    storage_overtime_df = session.sql(storage_overtime).to_pandas()
    fig_storage_overtime=px.bar(storage_overtime_df,x='USAGE_MONTH',y='BILLABLE_GB',color='BILLABLE_GB', orientation='v',title="Data Storage used Overtime", barmode="group")
    st.plotly_chart(fig_storage_overtime, use_container_width=True)

    st.divider()

    #############################################
    #  Storage by day in GB
    #############################################
    
    #Credits Usage (Total)
    storage_day_gb_sql = f"""
                                    
                    SELECT usage_date,
                    ROUND(storage_bytes / POWER(2, 30),3) AS TimeTravel_Storage_GB, 
                    ROUND(stage_bytes / POWER(2, 30),3) AS Internal_Stage_GB , 
                    ROUND(failsafe_bytes / POWER(2, 30),3) as Failsafe_GB
                    FROM SNOWFLAKE.ACCOUNT_USAGE.STORAGE_USAGE
                    WHERE usage_date between '{start_date}' and '{end_date}'                             
                                """
    pandas_storage_day_gb_df = session.sql(storage_day_gb_sql).to_pandas()
     
    #Chart
    fig_storage_day_gb=px.bar(pandas_storage_day_gb_df,x= 'USAGE_DATE',y=['TIMETRAVEL_STORAGE_GB','INTERNAL_STAGE_GB','FAILSAFE_GB'], barmode='group' ,orientation='v',title="Storage by day in GB")
    fig_storage_day_gb.update_layout(width=1000,height=600,legend =dict(orientation='h',yanchor='bottom',y=1.02,xanchor='center',x=0.5))
    #st.plotly_chart(fig_storage_day_gb, use_container_width=True)

    #############################################
    #  Storage by day in MB
    #############################################
    
    #Credits Usage (Total)
    storage_day_mb_sql = f"""
                                    
                    SELECT usage_date,
                    ROUND(storage_bytes / POWER(2, 30),2) AS TimeTravel_Storage_MB, 
                    ROUND(stage_bytes / POWER(2, 30),2) AS Internal_Stage_MB , 
                    ROUND(failsafe_bytes / POWER(2, 30),2) as Failsafe_MB
                    FROM SNOWFLAKE.ACCOUNT_USAGE.STORAGE_USAGE
                    WHERE usage_date between '{start_date}' and '{end_date}'                             
                                """
    pandas_storage_day_mb_df = session.sql(storage_day_mb_sql).to_pandas()
     
    #Chart
    fig_storage_day_mb=px.bar(pandas_storage_day_mb_df,x= 'USAGE_DATE',y=['TIMETRAVEL_STORAGE_MB','INTERNAL_STAGE_MB','FAILSAFE_MB'], barmode='group' ,orientation='v',title="Storage by day in MB")
    fig_storage_day_mb.update_layout(width=1000,height=600,legend =dict(orientation='h',yanchor='bottom',y=1.02,xanchor='center',x=0.5))
    #st.plotly_chart(fig_storage_day_mb, use_container_width=True)

    #Column formatting and metrics of header 3 metrics
    col1, col2= st.columns(2)
    col1.plotly_chart(fig_storage_day_gb, use_container_width=True)
    col2.plotly_chart(fig_storage_day_mb, use_container_width=True)
    
    #############################################
    #  Storage by Database in MB
    #############################################
    
    #Credits Usage (Total)
    storage_db_mb_sql = f"""
                        SELECT table_catalog as database_name, 
                            ROUND(SUM(active_bytes) / POWER(2, 20),2) AS Active_Storage_MB, --/ 30
                            ROUND(SUM(time_travel_bytes) / POWER(2, 20),2) AS Time_Travel_Storage_MB, 
                            ROUND(SUM(failsafe_bytes) / POWER(2, 20),2) AS Failsafe_Storage_MB, 
                            ROUND(SUM(retained_for_clone_bytes) / POWER(2, 20),2) AS Retained_For_Flone_Storage_MB,
                            Active_Storage_MB + Time_Travel_Storage_MB + Failsafe_Storage_MB + Retained_For_Flone_Storage_MB AS Total_Storage_MB
                        FROM snowflake.account_usage.table_storage_metrics
                        GROUP BY 1
                       ORDER BY  Total_Storage_MB asc                       
                                """
    pandas_storage_db_mb_df = session.sql(storage_db_mb_sql).to_pandas()
     
    #Chart,
    fig_storage_db_mb=px.bar(pandas_storage_db_mb_df,x= ['ACTIVE_STORAGE_MB','TIME_TRAVEL_STORAGE_MB','FAILSAFE_STORAGE_MB','RETAINED_FOR_FLONE_STORAGE_MB','TOTAL_STORAGE_MB'],y='DATABASE_NAME' ,orientation='h',title="Storage by Database in MB")
    fig_storage_db_mb.update_layout(width=1000,height=1000,legend =dict(orientation='h',yanchor='bottom',y=1.02,xanchor='center',x=0.5))
    st.plotly_chart(fig_storage_db_mb, use_container_width=True)

    #############################################
    #  Storage by Database in GB
    #############################################
    
    #Credits Usage (Total)
    storage_db_gb_sql = f"""
                        
                    SELECT table_catalog as database_name, 
                        ROUND(SUM(active_bytes) / POWER(2, 30),2) AS Active_Storage_GB, 
                        ROUND(SUM(time_travel_bytes) / POWER(2, 30),2) AS Time_Travel_Storage_GB, 
                        ROUND(SUM(failsafe_bytes) / POWER(2, 30),2) AS Failsafe_Storage_GB, 
                        ROUND(SUM(retained_for_clone_bytes) / POWER(2, 30),2) AS Retained_For_Flone_Storage_GB,
                        Active_Storage_GB + Time_Travel_Storage_GB + Failsafe_Storage_GB + Retained_For_Flone_Storage_GB AS Total_Storage_GB
                    FROM snowflake.account_usage.table_storage_metrics
                    GROUP BY 1
                    ORDER BY total_storage_GB asc
                     
                                """
    pandas_storage_db_gb_df = session.sql(storage_db_gb_sql).to_pandas()
     
    #Chart,
    fig_storage_db_gb=px.bar(pandas_storage_db_gb_df,x= ['ACTIVE_STORAGE_GB','TIME_TRAVEL_STORAGE_GB','FAILSAFE_STORAGE_GB','RETAINED_FOR_FLONE_STORAGE_GB','TOTAL_STORAGE_GB'],y='DATABASE_NAME' ,orientation='h',title="Storage by Database in GB")
    fig_storage_db_gb.update_layout(width=1000,height=1000,legend =dict(orientation='h',yanchor='bottom',y=1.02,xanchor='center',x=0.5))
    st.plotly_chart(fig_storage_db_gb, use_container_width=True)


    #############################################
    #  Short lived Tables
    #############################################
    
    #Credits Usage (Total)
    short_lived_table_sql = f""" select
                                concat(tm.table_catalog, '.', tm.table_schema) as schema_name,
                                case
                                    when datediff('seconds', tm.table_created, tm.table_dropped) < 30 then '1: < 30 sec'
                                    when datediff('seconds', tm.table_created, tm.table_dropped) < 60 then '2: < 1 min'
                                    when datediff('seconds', tm.table_created, tm.table_dropped) < 120 then '3: < 2 min'
                                    when datediff('seconds', tm.table_created, tm.table_dropped) < (60 * 3) then '4: < 3 min'
                                    when datediff('seconds', tm.table_created, tm.table_dropped) < (60 * 4) then '5: < 4 min'
                                    when datediff('seconds', tm.table_created, tm.table_dropped) < (60 * 5) then '6: < 5 min'
                                    when datediff('seconds', tm.table_created, tm.table_dropped) < (60 * 10) then '7: < 10 min'
                                    when datediff('seconds', tm.table_created, tm.table_dropped) < (60 * 30) then '8: < 30 min'
                                    when datediff('seconds', tm.table_created, tm.table_dropped) < (60 * 60) then '9: < 60 min'
                                    end as time_group,
                                count(*) as table_count
                            from snowflake.account_usage.table_storage_metrics tm
                            where
                                tm.deleted = true
                                and tm.table_created::date  between '{start_date}'::date and '{end_date}'::date
                                and tm.is_transient = 'NO'
                                and datediff('seconds', tm.table_created, tm.table_dropped) < (60 * 60)
                                and left(table_name, 3) <> 'TMP' and left(table_name, 4) <> 'TEMP' and right(table_name, 3) <> 'TMP' and right(table_name, 4) <> 'TEMP'
                            group by 1, 2
                            order by 2 desc

                            """
    pandas_short_lived_table_df = session.sql(short_lived_table_sql).to_pandas()
     
    #Chart
    fig_short_lived_table=px.bar(pandas_short_lived_table_df,x= 'TABLE_COUNT',y='SCHEMA_NAME',color='TIME_GROUP',orientation='h',title="Short lived Tables")
    fig_short_lived_table.update_traces(texttemplate = '%{x}',textfont = dict(size=14))
    fig_short_lived_table.update_layout(width=1000,height=600,legend =dict(orientation='h',yanchor='bottom',y=1.02,xanchor='center',x=0.5))
    st.plotly_chart(fig_short_lived_table, use_container_width=True)


    #############################################
    #     Rows Loaded Overtime (COPY INTO)                   
    #############################################
    
    rows_loaded = f"select to_timestamp(date_trunc(day,last_load_time)) as usage_date, sum(row_count) as total_rows from snowflake.account_usage.load_history where usage_date between '{start_date}'::date and '{end_date}'::date group by 1 order by usage_date desc"
    rows_loaded_df = session.sql(rows_loaded).to_pandas()
    
    fig_rows_loaded=px.bar(rows_loaded_df,x='USAGE_DATE',y='TOTAL_ROWS', orientation='v',title="Rows Loaded Overtime (Copy Into)")
    st.plotly_chart(fig_rows_loaded, use_container_width=True)

    #############################################
    #     FOOTER
    #############################################    
    st.divider()

##########################################################################################################################################################
####################################################   Performance Dashboard   ###########################################################################
##########################################################################################################################################################

with Performance_tab:

    st.header('Performance Dashboard')
    st.divider()
    
    #############################################
    #     Cards at Top
    #############################################

    # Total # of Jobs Executed
    num_jobs_sql = f"select count(*) as number_of_jobs from snowflake.account_usage.query_history where start_time between '{start_date}' and '{end_date}'"
    num_jobs_df = session.sql(num_jobs_sql)
    pandas_num_jobs_df = num_jobs_df.to_pandas()
    #Final Value
    num_jobs_tile = pandas_num_jobs_df.iloc[0].values
    #st.metric("Total # of Jobs Executed","{:,}".format(int(num_jobs_tile)))

    # Total Successfull Jobs Executed
    num_success_jobs_sql = f"select count(*) as number_of_jobs from snowflake.account_usage.query_history where start_time between '{start_date}' and '{end_date}' and execution_status = 'SUCCESS'"
    num_success_jobs_df = session.sql(num_success_jobs_sql)
    pandas_num_success_jobs_df = num_success_jobs_df.to_pandas()
    #Final Value
    num_success_jobs_tile = pandas_num_success_jobs_df.iloc[0].values
    #st.metric("Total # of Jobs Executed","{:,}".format(int(num_success_jobs_tile)))

    # Total failed Jobs
    num_failed_jobs_sql = f"select count(*) as number_of_jobs from snowflake.account_usage.query_history where start_time between '{start_date}' and '{end_date}' and execution_status = 'FAIL'"
    num_failed_jobs_df = session.sql(num_failed_jobs_sql)
    pandas_num_failed_jobs_df = num_failed_jobs_df.to_pandas()
    #Final Value
    num_failed_jobs_tile = pandas_num_failed_jobs_df.iloc[0].values
    #st.metric("Total # of Jobs Executed","{:,}".format(int(num_failed_jobs_tile)))

    #Column formatting and metrics of header 3 metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total # of Jobs Executed","{:,}".format(int(num_jobs_tile)))
    col2.metric("Total Successfull Jobs Executed","{:,}".format(int(num_success_jobs_tile)))
    col3.metric("Total failed Jobs","{:,}".format(int(num_failed_jobs_tile)))

    #############################################
    #  Query Execution by Time Bucket (Bar Chart)
    #############################################
    
    #Credits Usage (Total)
    query_Execution_sql = f"""select
                            case
                                when qh.execution_time < 10000 then '1: < 10 sec'
                                when qh.execution_time < 60000 then '2: < 1 min'
                                when qh.execution_time < 300000 then '3: < 5 min'
                                when qh.execution_time < 600000 then '4: < 10 min'
                                when qh.execution_time < 1800000 then '5: < 30 min'
                                when qh.execution_time < 3600000 then '6: < 60 min'
                                when qh.execution_time >= 3600000 then '7: >= 1 hour'
                                end as time_group,
                            count(*) as query_count
                        from snowflake.account_usage.query_history qh
                        where
                            qh.start_time::date between '{start_date}' and '{end_date}' 
                        
                            and qh.execution_time is not null and qh.execution_time > 0
                            and qh.warehouse_size is not null
                        group by 1
                        order by time_group desc """
    pandas_query_Execution_df = session.sql(query_Execution_sql).to_pandas()
     
    #Chart
    fig_query_Execution=px.bar(pandas_query_Execution_df,x= 'QUERY_COUNT',y='TIME_GROUP',orientation='h',title="Query Execution by Time Bucket")
    fig_query_Execution.update_traces(texttemplate = '%{x}',textfont = dict(size=14))
    st.plotly_chart(fig_query_Execution, use_container_width=True)

    #############################################
    #  Query Compilation Stats (Bar Chart)
    #############################################
    
    #Credits Usage (Total)
    query_Compilation_sql = f"""select
                                case
                                    when qh.compilation_time < 10000 then '1: < 10 sec'
                                    when qh.compilation_time < 60000 then '2: < 1 min'
                                    when qh.compilation_time < 300000 then '3: < 5 min'
                                    when qh.compilation_time < 600000 then '4: < 10 min'
                                    when qh.compilation_time < 1800000 then '5: < 30 min'
                                    when qh.compilation_time < 3600000 then '6: < 60 min'
                                    when qh.compilation_time >= 3600000 then '7: >= 1 hour'
                                    end as time_group,
                                count(*) as query_count
                            from snowflake.account_usage.query_history qh
                            where
                                qh.start_time between '{start_date}' and '{end_date}'                             
                                and qh.compilation_time is not null and qh.compilation_time > 0
                                and qh.warehouse_size is not null
                            group by 1 
                            order by 1 desc"""
    pandas_query_Compilation_df = session.sql(query_Compilation_sql).to_pandas()
     
    #Chart
    fig_query_Compilation=px.bar(pandas_query_Compilation_df,x= 'QUERY_COUNT',y='TIME_GROUP',orientation='h',title="Query Compilation Stats")
    fig_query_Compilation.update_traces(texttemplate = '%{x}',textfont = dict(size=14))
    st.plotly_chart(fig_query_Compilation, use_container_width=True)

    #############################################
    #  Query Queued Stats (Bar Chart)
    #############################################
    
    #Credits Usage (Total)
    query_Queued_Stats_sql = f"""
                                select
                                    case
                                        when qh.queued_overload_time < 10000 then '1: < 10 sec'
                                        when qh.queued_overload_time < 60000 then '2: < 1 min'
                                        when qh.queued_overload_time < 300000 then '3: < 5 min'
                                        when qh.queued_overload_time < 600000 then '4: < 10 min'
                                        when qh.queued_overload_time < 1800000 then '5: < 30 min'
                                        when qh.queued_overload_time < 3600000 then '6: < 60 min'
                                        when qh.queued_overload_time >= 3600000 then '7: >= 1 hour'
                                        end as time_group,
                                    count(*) as query_count
                                from snowflake.account_usage.query_history qh
                                where
                                    qh.start_time between '{start_date}' and '{end_date}'
                                    and qh.execution_time is not null and qh.execution_time > 0
                                    and qh.warehouse_size is not null
                                group by 1
                                """
    pandas_query_Queued_Stats_df = session.sql(query_Queued_Stats_sql).to_pandas()
     
    #Chart
    fig_query_Queued_Stats=px.bar(pandas_query_Queued_Stats_df,x= 'QUERY_COUNT',y='TIME_GROUP',orientation='h',title="Query Queued Stats")
    fig_query_Queued_Stats.update_traces(texttemplate = '%{x}',textfont = dict(size=14))
    st.plotly_chart(fig_query_Queued_Stats, use_container_width=True)

    #############################################
    # Query Execution by Time Bucket by Warehouse
    #############################################
    
    #Credits Usage (Total)
    query_Execution_wh_sql = f"""select
                                    case
                                        when qh.execution_time < 10000 then '1: < 10 sec'
                                        when qh.execution_time < 60000 then '2: < 1 min'
                                        when qh.execution_time < 300000 then '3: < 5 min'
                                        when qh.execution_time < 600000 then '4: < 10 min'
                                        when qh.execution_time < 1800000 then '5: < 30 min'
                                        when qh.execution_time < 3600000 then '6: < 60 min'
                                        when qh.execution_time >= 3600000 then '7: >= 1 hour'
                                        end as time_group,
                                    qh.warehouse_name as warehouse_name,
                                    count(*) as query_count
                                from snowflake.account_usage.query_history qh
                                where
                                    qh.start_time between '{start_date}' and '{end_date}'
                                    and qh.execution_time is not null and qh.execution_time > 0
                                    and qh.warehouse_size is not null
                                group by 1, 2
                                order by time_group desc"""
    pandas_query_Execution_wh_df = session.sql(query_Execution_wh_sql).to_pandas()
     
    #Chart
    fig_query_Execution_wh=px.bar(pandas_query_Execution_wh_df,x='QUERY_COUNT',y='TIME_GROUP',color='WAREHOUSE_NAME' ,orientation='h',title="Query Execution by Time Bucket by Warehouse")
    #fig_query_Execution_wh.update_traces(showlegend=False)
    fig_query_Execution_wh.update_layout(width=1000,height=600)
    st.plotly_chart(fig_query_Execution_wh, use_container_width=True)


    #############################################
    # Query Execution by Time Bucket by Warehouse
    #############################################
    
    #Credits Usage (Total)
    query_Execution_wh_sql = f"""select
                                    case
                                        when qh.execution_time < 10000 then '1: < 10 sec'
                                        when qh.execution_time < 60000 then '2: < 1 min'
                                        when qh.execution_time < 300000 then '3: < 5 min'
                                        when qh.execution_time < 600000 then '4: < 10 min'
                                        when qh.execution_time < 1800000 then '5: < 30 min'
                                        when qh.execution_time < 3600000 then '6: < 60 min'
                                        when qh.execution_time >= 3600000 then '7: >= 1 hour'
                                        end as time_group,
                                    qh.warehouse_name as warehouse_name,
                                    count(*) as query_count
                                from snowflake.account_usage.query_history qh
                                where
                                    qh.start_time between '{start_date}' and '{end_date}'
                                    and qh.execution_time is not null and qh.execution_time > 0
                                    and qh.warehouse_size is not null
                                group by 1, 2
                                order by time_group desc"""
    pandas_query_Execution_wh_df = session.sql(query_Execution_wh_sql).to_pandas()
     
    #Chart
    fig_query_Execution_wh=px.bar(pandas_query_Execution_wh_df,x='QUERY_COUNT',y='WAREHOUSE_NAME',color='TIME_GROUP' ,orientation='h',title="Query Execution by Time Bucket by Warehouse")
    #fig_query_Execution_wh.update_traces(showlegend=False)
    fig_query_Execution_wh.update_layout(width=1000,height=600,legend =dict(orientation='h',yanchor='bottom',y=1.02,xanchor='center',x=0.5))
    st.plotly_chart(fig_query_Execution_wh, use_container_width=True)



    #############################################
    #  Query Compilation Stats  by Warehouse
    #############################################
    
    #Credits Usage (Total)
    query_Compilation_wh_sql = f"""select
                                case
                                    when qh.compilation_time < 10000 then '1: < 10 sec'
                                    when qh.compilation_time < 60000 then '2: < 1 min'
                                    when qh.compilation_time < 300000 then '3: < 5 min'
                                    when qh.compilation_time < 600000 then '4: < 10 min'
                                    when qh.compilation_time < 1800000 then '5: < 30 min'
                                    when qh.compilation_time < 3600000 then '6: < 60 min'
                                    when qh.compilation_time >= 3600000 then '7: >= 1 hour'
                                    end as time_group,
                                    qh.warehouse_name as warehouse_name,
                                count(*) as query_count
                            from snowflake.account_usage.query_history qh
                            where
                                qh.start_time between '{start_date}' and '{end_date}'                             
                                and qh.compilation_time is not null and qh.compilation_time > 0
                                and qh.warehouse_size is not null
                            group by 1 ,2
                            order by 1 desc,2"""
    pandas_query_Compilation_wh_df = session.sql(query_Compilation_wh_sql).to_pandas()
     
    #Chart
    fig_query_Compilation_wh=px.bar(pandas_query_Compilation_wh_df,x= 'QUERY_COUNT',y='TIME_GROUP',color='WAREHOUSE_NAME', barmode='group' ,orientation='h',title="Query Compilation Stats")
    fig_query_Compilation_wh.update_layout(width=1000,height=600)
    st.plotly_chart(fig_query_Compilation_wh, use_container_width=True)

    #############################################
    #  Query Compilation Stats by Warehouse
    #############################################
    
    #Credits Usage (Total)
    query_Queued_Stats_wh_sql = f"""
                                select
                                    case
                                        when qh.queued_overload_time < 10000 then '1: < 10 sec'
                                        when qh.queued_overload_time < 60000 then '2: < 1 min'
                                        when qh.queued_overload_time < 300000 then '3: < 5 min'
                                        when qh.queued_overload_time < 600000 then '4: < 10 min'
                                        when qh.queued_overload_time < 1800000 then '5: < 30 min'
                                        when qh.queued_overload_time < 3600000 then '6: < 60 min'
                                        when qh.queued_overload_time >= 3600000 then '7: >= 1 hour'
                                        end as time_group,
                                    qh.warehouse_name as warehouse_name,
                                    count(*) as query_count
                                from snowflake.account_usage.query_history qh
                                where
                                    qh.start_time between '{start_date}' and '{end_date}'
                                    and qh.execution_time is not null and qh.execution_time > 0
                                    and qh.warehouse_size is not null
                                group by 1,2
                                """
    pandas_query_Queued_Stats_wh_df = session.sql(query_Queued_Stats_wh_sql).to_pandas()
     
    #Chart
    fig_query_Queued_Stats_wh=px.bar(pandas_query_Queued_Stats_wh_df,x= 'QUERY_COUNT',y='TIME_GROUP',color='WAREHOUSE_NAME', barmode='group' ,orientation='h',title="Query Compilation Stats by Warehouse")
    fig_query_Queued_Stats_wh.update_traces(texttemplate = '%{x}',textfont = dict(size=14))
    st.plotly_chart(fig_query_Queued_Stats_wh, use_container_width=True)

    #############################################
    #  Queries by Role
    #############################################
    
    #Credits Usage (Total)
    query_by_Role_sql = f"""
                            select
                                date_trunc('day', qh.start_time)::date as usage_date,
                                qh.role_name,
                                count(*) as query_count
                            from snowflake.account_usage.query_history qh
                            where
                                qh.start_time::date  between '{start_date}'::date and '{end_date}'::date
                                and (qh.role_name ilike 'AAD%' or qh.role_name ilike '%ETLSVC% ' or qh.role_name ilike '%ADMIN'or qh.role_name ilike '%PROFILE%')
                            group by 1, 2 
                            """
    pandas_query_by_Role_df = session.sql(query_by_Role_sql).to_pandas()
     
    #Chart
    fig_query_by_Role=px.bar(pandas_query_by_Role_df,x= 'USAGE_DATE',y='QUERY_COUNT',color='ROLE_NAME', barmode='group',orientation='v',title="Queries by Role")
    fig_query_by_Role.update_traces(texttemplate = '%{y}',textfont = dict(size=14))
    st.plotly_chart(fig_query_by_Role, use_container_width=True)

    #############################################
    #  Queries by Role
    #############################################
    
    #Credits Usage (Total)
    query_by_Role_sql = f"""with ranked_data as (
            select
                date_trunc('day', qh.start_time)::date as usage_date,
                qh.role_name,
                count(*) as query_count,
                rank() over (partition by usage_date order by query_count desc ) as role_rank
            from snowflake.account_usage.query_history qh
            where qh.start_time::date between '{start_date}'::date and '{end_date}'::date
            and (qh.role_name ilike 'AAD%' or qh.role_name ilike '%ETLSVC% ' or qh.role_name ilike '%ADMIN'or qh.role_name ilike '%PROFILE%')
            group by 1, 2
            )
            
            select 
                usage_date,
                case when role_rank <= 5 then role_name else 'Other' end as role_group,
                sum(query_count) as query_count
            from ranked_data
            group by 1,2
            order by 1 desc,3 desc
                            """
    pandas_query_by_Role_df = session.sql(query_by_Role_sql).to_pandas()
     
    #Chart
    fig_query_by_Role=px.bar(pandas_query_by_Role_df,x= 'USAGE_DATE',y='QUERY_COUNT',color='ROLE_GROUP', barmode='group',orientation='v',title="Queries by Role")
    st.plotly_chart(fig_query_by_Role, use_container_width=True)

    #############################################
    #  Average Execution by Query Type
    #############################################
    
    execution_by_qtype = f"""select query_type, warehouse_size, round(avg(execution_time) / 60000,2) as average_execution_time 
                            from snowflake.account_usage.query_history 
                            where start_time between '{start_date}' and '{end_date}' 
                            group by 1, 2 order by 3 asc"""
    execution_by_qtype_df = session.sql(execution_by_qtype)
    pandas_execution_by_qtype_df = execution_by_qtype_df.to_pandas()
    fig_execution_by_qtype=px.bar(pandas_execution_by_qtype_df,x='AVERAGE_EXECUTION_TIME',y='QUERY_TYPE',orientation='h',title="Average Execution by Query Type")
    fig_execution_by_qtype.update_layout(width=1000,height=600)
    st.plotly_chart(fig_execution_by_qtype, use_container_width=True)


    #############################################
    #     Top 25 Longest Queries (Success)
    #############################################
    
    #Top 25 Longest Queries (Success)
    longest_queries_sql = f"select query_id,left(query_text,30) as query_text,(execution_time / 60000) as exec_time from snowflake.account_usage.query_history where execution_status = 'SUCCESS' and start_time between '{start_date}' and '{end_date}'  order by execution_time desc limit 25"
    longest_queries_df = session.sql(longest_queries_sql)
    
    #convert to pandas df
    pandas_longest_queries_df = longest_queries_df.to_pandas()
    
    #chart
    fig_longest_queries=px.bar(pandas_longest_queries_df,x='EXEC_TIME',y='QUERY_TEXT',orientation='h',title="Longest Successful Queries (Top 25) ")
    
    #st.write(fig_longest_queries)
    
    #############################################
    #     Top 25 Longest Queries (Failed)
    #############################################
    
    #Top 25 Longest Queries (Failed)
    f_longest_queries_sql = f"select query_id,left(query_text,30) as query_text,(execution_time / 60000) as exec_time from snowflake.account_usage.query_history where execution_status = 'FAIL' and start_time between '{start_date}' and '{end_date}' order by execution_time desc limit 25"
    f_longest_queries_df = session.sql(longest_queries_sql)
    
    #convert to pandas df
    f_pandas_longest_queries_df = longest_queries_df.to_pandas()
    
    #chart
    fig_f_longest_queries=px.bar(f_pandas_longest_queries_df,x='EXEC_TIME',y='QUERY_TEXT',orientation='h',title="Longest Failed Queries (Top 25)")
    fig_f_longest_queries.update_traces(marker_color='red')
    
    #st.write(fig_f_longest_queries)
    
    
    
    #############################################
    #  Top 25 Query Success/Failure
    #############################################
    
    container2 = st.container()
    
    with container2:
        plot1, plot2 = st.columns(2)
        with plot1:
            st.plotly_chart(fig_longest_queries, use_container_width=True)
        with plot2:
            st.plotly_chart(fig_f_longest_queries, use_container_width=True)


    #############################################
    #     Total Execution Time by Repeated Queries
    #############################################
    
    total_execution_time_sql = f"select left(query_text,30) as query_text, (sum(execution_time) / 60000) as exec_time from snowflake.account_usage.query_history where execution_status = 'SUCCESS' and start_time between '{start_date}' and '{end_date}' group by query_text order by exec_time desc limit 10"
    total_execution_time_df = session.sql(total_execution_time_sql).to_pandas()
    #st.write(total_execution_time_df)
    fig_execution_time=px.bar(total_execution_time_df,x='EXEC_TIME',y='QUERY_TEXT', orientation='h',title="Total Execution Time by Repeated Queries")
    fig_execution_time.update_traces(marker_color='LightSkyBlue')
    fig_execution_time.update_traces(texttemplate = '%{x}',textfont = dict(size=14))
    
    st.plotly_chart(fig_execution_time, use_container_width=True)

    #############################################
    #  Top 10 Average Query Execution Time (By User)
    #############################################
    
    query_execution = "select user_name, (avg(execution_time)) / 1000 as average_execution_time from snowflake.account_usage.query_history group by 1 order by 2 desc limit 10"
    query_execution_df = session.sql(query_execution).to_pandas()
    #st.write(query_execution_df)
    fig_cquery_execution=px.bar(query_execution_df,x='USER_NAME',y='AVERAGE_EXECUTION_TIME', orientation='v',title="Average Execution Time per User")
    fig_cquery_execution.update_traces(marker_color='MediumPurple')
    st.plotly_chart(fig_cquery_execution,use_container_width=True)

    #############################################
    #     FOOTER
    #############################################    
    st.divider()
