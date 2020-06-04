import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from datetime import timedelta
import plotly
import chart_studio.plotly as py
import numpy as np
py.sign_in('nishtha697','RgHrQxWQq9hp2PQofsUg')
import plotly.graph_objs as go

@st.cache(ttl=60*5,max_entries=20)
def load_state_daily():
    state_daily = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")
    return state_daily

state_daily = load_state_daily()

@st.cache(ttl=60*5,max_entries=20)
def load_district_data():
    district_data = pd.read_csv("https://api.covid19india.org/csv/latest/district_wise.csv")
    return district_data

district_data = load_district_data()

@st.cache(ttl=60*60*2,max_entries=20)
def load_state_data():
    state_data = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise_daily.csv	")
    state_data['Date'] = pd.to_datetime(state_data['Date'])
    return state_data

state_data = load_state_data()

def get_total_dataframe(dataset):
    total_dataframe = pd.DataFrame({'Status':['Confirmed', 'Active', 'Recovered', 'Deaths'],
    'Number of cases':(dataset.iloc[0]['Confirmed'],
    dataset.iloc[0]['Active'], dataset.iloc[0]['Recovered'],
    dataset.iloc[0]['Deaths'])})
    return total_dataframe

def get_today_dataframe(dataset):
    today_dataframe = pd.DataFrame({'Status':['Confirmed', 'Recovered', 'Deaths'],
    'Number of cases':(dataset.iloc[0]['Delta_Confirmed'], dataset.iloc[0]['Delta_Recovered'],
    dataset.iloc[0]['Delta_Deaths'])})
    return today_dataframe

def get_top_states(original_data, number, select_status):
    if select_status == 'Confirmed':
        st.write(original_data.query("Confirmed >= 1")[["State", "Confirmed"]].sort_values(by=['Confirmed'], ascending=False).dropna(how='any')[:number])
    elif select_status == 'Active':
        st.write(original_data.query("Active >= 1")[["State", "Active"]].sort_values(by=['Active'], ascending=False).dropna(how='any')[:number])
    elif select_status == 'Recovered':
        st.write(original_data.query("Active >= 1")[["State", "Recovered"]].sort_values(by=['Recovered'], ascending=False).dropna(how='any')[:number])
    else:
        st.write(original_data.query("Deceased >= 1")[["State", "Deceased"]].sort_values(by=['Deaths'], ascending=False).dropna(how='any')[:number])

def get_table():
    datatable = state_daily[['State', 'Confirmed', 'Active', 'Recovered', 'Deaths']].sort_values(by=['Confirmed'], ascending=False)
    datatable = datatable[datatable['State'] != 'State Unassigned']
    return datatable


st.markdown('<body style="background-color:powderblue;">', unsafe_allow_html=True)
st.title('🦠 Covid-19 Impact in India')
st.markdown('This app gives you the realtime impact analysis of Covid-19 in India. You can gt')

st.sidebar.title('Select the parameters to analyze Covid-19 situation')
india_checkbox = st.sidebar.checkbox("Show Overall Analysis", True, key=11)
if not india_checkbox:
    st.sidebar.markdown("<sup>The graphical representations for India are hidden as the above checkbox is unchecked</sup>", unsafe_allow_html=True)

st.sidebar.subheader("State wise analysis")
state_checkbox = st.sidebar.checkbox("Show Analysis by State", True, key=3)
if not state_checkbox:
    st.sidebar.markdown("<sup>The graphical representations for States are hidden as the above checkbox is unchecked</sup>", unsafe_allow_html=True)

st.markdown('<style>sup{color: red;}</style>', unsafe_allow_html=True)

select = st.sidebar.selectbox('State',["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep", "Ladakh", "National Capital Territory of Delhi","Puducherry"])

states = {'Andhra Pradesh': 'AP',
'Arunachal Pradesh': 'AR',
'Assam': 'AS',
'Bihar': 'BR',
'Chhattisgarh': 'CT',
"Goa": 'GA',
"Gujarat": 'GJ',
"Haryana": 'HR',
"Himachal Pradesh": 'HP',
"Jammu and Kashmir": "JK",
"Jharkhand": "JH",
"Karnataka": "KA",
"Kerala": "KL",
"Madhya Pradesh": "MP",
"Maharashtra": "MH",
"Manipur": "MN",
"Meghalaya":"ML",
"Mizoram": "MZ",
"Nagaland": "NL",
"Odisha": "OR",
"Punjab": "PB",
"Rajasthan": "RJ" ,
"Sikkim": "SK",
"Tamil Nadu": "TN",
"Telangana": "TG",
"Tripura": "TR",
"Uttar Pradesh": "UP",
"Uttarakhand": "UT",
"West Bengal": "WB",
"Andaman and Nicobar Islands": "AN",
"Chandigarh": "CH",
"Dadra and Nagar Haveli": "DN",
"Daman and Diu": "DD",
"Lakshadweep": "LD",
"Ladakh": "LA",
"National Capital Territory of Delhi": "DL",
"Puducherry": "PY"}

india_data = state_daily[state_daily['State'] == 'Total']
india_total = get_total_dataframe(india_data)
india_today = get_today_dataframe(india_data)

if india_checkbox:
    st.markdown("# Overall Analysis For India")
    st.markdown("### Total Confirmed, Total Recovered and Total Deceased cases in India yet")
    if not st.checkbox('Hide', False, key=1):
        india_total_chart = px.histogram(india_total, x='Status', y='Number of cases', color='Status', width=700)
        st.plotly_chart(india_total_chart)

    st.markdown("### Confirmed, Recovered and Deceased cases in India today")
    if not st.checkbox('Hide', False, key=2):
        india_today_chart = px.bar(india_today, x='Status', y='Number of cases', color='Status', width=700)
        st.plotly_chart(india_today_chart)

    datatable = get_table()
    st.markdown("### Covid-19 cases in India")
    st.write(datatable)

state_wise_data = state_daily[state_daily['State_code'] == states[select]]
state_wise_total = get_total_dataframe(state_wise_data)
state_wise_today = get_today_dataframe(state_wise_data)

confirmed = state_data[state_data['Status'] == 'Confirmed']
recovered = state_data[state_data['Status'] == 'Recovered']
deceased = state_data[state_data['Status'] == 'Deceased']

modified_data = district_data[district_data['State'] == select]

st.sidebar.subheader("States with most covid-19 cases")
top_states = st.sidebar.slider("Number of states:", 1, 28)
select_status = st.sidebar.selectbox("Covid-19 patient status", ('Confirmed', 'Active', 'Recovered', 'Deceased'))
st.sidebar.markdown("---")
filtered_state_daily = state_daily[state_daily['State'] != 'Total']

if state_checkbox:
    st.markdown("# State level Analysis")

    st.markdown("### Total Confirmed, Total Recovered and Total Deceased cases in %s yet" % (select))
    if not st.checkbox('Hide', False, key=4):
        state_total = px.histogram(state_wise_total, x='Status', y='Number of cases', labels={'Number of cases':'number of cases in %s' % (select)}, color='Status', width=700)
        st.plotly_chart(state_total)

    st.markdown("### Confirmed, Recovered and Deceased cases in %s today" % (select))
    if not st.checkbox('Hide', False, key=5):
        state_today = px.bar(state_wise_today, x='Status', y='Number of cases', labels={'Number of cases':'Number of cases in %s' % (select)}, color='Status', width=700)
        st.plotly_chart(state_today)

    st.subheader("Number of cases Confirmed, Recovered and Deceased in %s over time" % (select))

    if not st.checkbox('Hide', False, key=6):
        select_visual = st.selectbox("Visualization type", ("Line chart", "Histogram"))
        if(select_visual == 'Line chart'):
            figure = go.Figure()
            figure.add_trace(go.Scatter(x=confirmed.Date, y=confirmed[states[select]],
                                mode='lines',
                                name='Confirmed'))
            figure.add_trace(go.Scatter(x=recovered.Date, y=recovered[states[select]],
                                mode='lines',
                                    name='Recovered'))
            figure.add_trace(go.Scatter(x=deceased.Date, y=deceased[states[select]],
                                mode='lines', name='Deceased'))
            figure.update_layout(
                autosize=False,
                width=900,
                height=600,
                yaxis=dict(
                    title_text="Number of cases",
                ),
                xaxis=dict(
                    title_text="Date",
                )
            )
            st.plotly_chart(figure)

        else:
            fig_choice = px.histogram(state_data, x='Date', y=states[select], color='Status',
            facet_row='Status', height=600, width=800, labels={states[select]:"corona cases"})
            st.plotly_chart(fig_choice)

    st.subheader("Top %i State(s) with most %s covid-19 patients" % (top_states, select_status))
    get_top_states(filtered_state_daily, top_states, select_status)

districts = ['All Districts']
uniqueDistricts = modified_data['District'].unique()

for district in uniqueDistricts:
   districts.append(district)

st.sidebar.subheader("District wise analysis")
district_checkbox = st.sidebar.checkbox("Show Analysis by District", True, key=7)
if not district_checkbox:
    st.sidebar.markdown("<sup>The graphical representations for Districts are hidden as the above checkbox is unchecked</sup>", unsafe_allow_html=True)
select_district = st.sidebar.selectbox('District (of the State selected above)', districts)
selected_district_data = district_data[district_data['District'] == select_district]

ds = []
numbers = []
status = []
for d in uniqueDistricts:
    for i in range(0,4):
        ds.append(d)
    data = modified_data[modified_data['District'] == d]
    numbers.extend([data.iloc[0]['Confirmed'], data.iloc[0]['Active'], data.iloc[0]['Recovered'],
    data.iloc[0]['Deceased']])
    status.extend(['Confirmed', 'Active', 'Recovered', 'Deceased'])

modified_dataframe = pd.DataFrame({'District': ds, 'Status': status, 'Number': numbers})

st.sidebar.subheader("Districts with more following number of cases")
slider = st.sidebar.slider("Number of cases", 0, 10000)
radio_state = st.sidebar.radio("Status", ('Confirmed', 'Active', 'Recovered', 'Deceased'))

filtered_district_data = district_data[district_data[radio_state] >= slider]
filtered_district_data = filtered_district_data[['District', 'State', radio_state]]
filtered_district_data = filtered_district_data[filtered_district_data['District'] != 'Unknown']
filtered_district_data = filtered_district_data[filtered_district_data['District'] != 'Unassigned']

if district_checkbox:
    st.markdown("# District level Analysis")
    st.subheader("Breakdown %s Covid-19 cases by district from May 24th onwards" % (select))
    if not st.checkbox('Hide', False, key=8):
        fig_choice = px.histogram(modified_dataframe, x='District', y='Number', color='District',
        facet_col='Status', labels={'Current Status':'Status', 'Detected District': 'District'}, height=600, width=900)
        st.plotly_chart(fig_choice)
        #st.write(modified_data)


    if select_district != 'All Districts':
        district_dataframe = pd.DataFrame({'Status':['Confirmed', 'Active', 'Recovered', 'Deceased'], 'Number of cases':(selected_district_data.iloc[0]['Confirmed'],
        selected_district_data.iloc[0]['Active'], selected_district_data.iloc[0]['Recovered'], selected_district_data.iloc[0]['Deceased'])})
        district_dataframe_today = pd.DataFrame({'Status':['Confirmed', 'Active', 'Recovered', 'Deceased'],
        'Number of cases':(selected_district_data.iloc[0]['Delta_Confirmed'], selected_district_data.iloc[0]['Delta_Active'], selected_district_data.iloc[0]['Delta_Recovered'], selected_district_data.iloc[0]['Delta_Deceased'])})

        st.markdown("### Total Confirmed, Total Recovered and Total Deceased cases in %s district yet" % (select_district))
        if not st.checkbox('Hide', False, key=9):
            district_fig = px.bar(district_dataframe, x='Status', y='Number of cases', color='Status' )
            st.plotly_chart(district_fig)

        st.markdown("### Confirmed, Recovered and Deceased cases in %s district today" % (select_district))
        if not st.checkbox('Hide', False, key=10):
            district_fig = px.bar(district_dataframe_today, x='Status', y='Number of cases', color='Status' )
            st.plotly_chart(district_fig)


    st.markdown("### Districts with more than %i %s cases" % (slider, radio_state))

    if filtered_district_data.empty:
        st.write("There are no districts with more than or equal to %i %s cases" % (slider, radio_state))
    else:
        st.write(filtered_district_data)
st.markdown('</body>', unsafe_allow_html=True)
