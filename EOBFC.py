import pandas as pd 
import matplotlib.pyplot as plt 
import plotly.express as px 
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(page_title='EOBFC Fines', page_icon='⚽', layout='wide')
st.title('EOBFC Fines 2025-26 ⚽💰')

st.divider()

#Define filepath
filepath = pd.ExcelFile(r'C:\Users\dofoe.boundarycreek\Documents\Python Output\EOBFC\EOBFC fines list 25_26.xlsx')

#List of sheet names
sheet_names = ['GW1', 'GW2', 'GW3', 'GW4', 'GW5']

def clean_data(df): 
    df = df.iloc[0:20, ].drop('Amount', axis='columns')
    df = df.set_index('Fine')
    df = df.dropna(how='all').dropna(axis='columns', how='all')
    return df

def main(): 
    cleaned_dataframes = {} 

    for sheet in sheet_names: 
        df = pd.read_excel(filepath, sheet_name=sheet)
        cleaned_df = clean_data(df)
        cleaned_dataframes[sheet] = cleaned_df


    combined_df = pd.concat(cleaned_dataframes.values(), ignore_index=False).groupby('Fine').sum() 
    #combined_df.loc['Total'] = combined_df.sum()


    tab1, tab2, tab3, tab4 = st.tabs(['Individual Stats', 'Sorted Table', 'Total Sum by Category', 'Fine Frequency'])
    with tab1:
        #Add Sidebar 
        st.sidebar.title('Geezers')
        names_list = combined_df.columns.to_list() 
        selected_name = st.sidebar.multiselect('Select a Legend!', options=names_list, default=None)

        all_options = st.sidebar.checkbox('Select all options', value=False)
        if all_options: 
            selected_name = names_list

        #Filtered data 
        col_header = ['Amount']
        total_per_name = combined_df[selected_name].sum()
        total_df = pd.DataFrame(total_per_name, columns=col_header)
        total_df = total_df['Amount'].sum() 
        st.metric('Total Amount', f'£{total_df}')
        if selected_name:
            st.dataframe(
                combined_df[selected_name],
                height=540,
                )

            #Visualisation 
            st.bar_chart(combined_df[selected_name])
        else: 
            st.info('Use the dropdown to see the data.')

    with tab2: 
        st.subheader('Total Contributions so Far...')
        total_squad = combined_df.sum().sort_values(ascending=False) 
        total_squad = pd.DataFrame(total_squad, columns=col_header)
        st.write(total_squad)

    with tab3: 
      sum_df = combined_df[combined_df != 0].sum(axis='columns')  
      sum_df = pd.DataFrame(sum_df, columns=col_header)
      
      fig = go.Figure(data=go.Bar(
      x=sum_df.index, 
      y=sum_df['Amount'],
      text=sum_df['Amount']
      ))

      fig.update_layout(
          title='EOBFC Fines by Category',
          yaxis_title='Amount',
          width=500,
          height=750
      )
      fig.update_traces(marker_color="#04a040", textposition='outside')

      st.plotly_chart(fig)


      with tab4: 
          count_df = combined_df[combined_df != 0].count(axis='columns')
          count_df = pd.DataFrame(count_df, columns=col_header)
          
          line = go.Figure(data=go.Scatter(
              x=count_df.index,
              y=count_df['Amount'],
              line=dict(color='#ff9900', width=2)
          ))
          line.update_layout(
              title='Frequency of Offence', 
              yaxis_title='Frequency Count'
          )

          st.plotly_chart(line)

main()


