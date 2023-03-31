import streamlit as st
import pandas as pd
from datetime import date
import calendar
import warnings
import base64
import openpyxl


warnings.filterwarnings('ignore')

# This function removes the first three rows, and the first column.
# Next it assigns the new first row as column labels.
# Returns the modified data frame.
# Returns the modified dataframe.
def bring_to_template(df_input):
  df_input = df_input.iloc[:, 1:]
  df_input = df_input.drop([0, 1])
  df_input = df_input.rename(columns = df_input.iloc[0])
  df_input = df_input.iloc[1: , :]
  df_input = pd.DataFrame(df_input)
  return df_input

# It checks there is a Tech Telephone #, 
# If yes, '+1' concats with it.
# If no, it checks if there is a Tech Mobile #.
# If yes, '+1' gets concatinated and added to Tech Telephone #
# If no, it's a blank cell.
# Returns the modified dataframe
def modify_telephone(df):
  for i in range(len(df)):
    if df['Site Tech Tel#'].iloc[i] == "() -" and df['Site Tech Mobile#'].iloc[i] != "() -":
      df['Site Tech Tel#'].iloc[i] = "+1 " + df['Site Tech Mobile#'].iloc[i]
    elif df['Site Tech Tel#'].iloc[i] != "() -":
      df['Site Tech Tel#'].iloc[i] = "+1 " + df['Site Tech Tel#'].iloc[i]
    else:
      df['Site Tech Tel#'].iloc[i] = ""
  return df

# Renaming the columns to the dashboard variables.
# Returns the modified dataframe.

def rename_cols(df):
  df.rename(columns = {'Site Location Code': 'Site Code', 'Region':'Site Region', 'Site Tech Tel#' : 'Site Tech Phone', 'Site Tower Height': 'Tower Height', 'Site Structure Type': 'Tower Type', 'Site Tech Email': 'Site Tech E-mail'}, inplace=True)
  return df

# Removing the unncessary cells.
# Returns the modified dataframe.

def remove_the_cols(df):
  df = df[['Site Code', 'Site EMG', 'Site Region', 'Site Name', 'Site Adress', 'Site City', 'Coordinates', 'Site Tech', 'Site Tech Phone', 'Site Tech E-mail', 'Tower Type', 'Tower Height', 'Site Directions', 'Special Dispatch Instructions']]
  return df

# Merges long and lat into a new column called coordinates.
# Returns the modified Dataframe.

def merge_lat_long(df):
  df['Coordinates'] = df['Site Longitude'] + "" + df['Site Latitude']
  return df

# Concats @rci.rogers.com to the email. Changes column name from Tech Email to
# Tech E-mail
# Returns modified dataframe
def modify_email(df):
  df['Site Tech Email'] = df['Site Tech Email'] + "@rci.rogers.com"
  return df

def get_table_download_link(df):
    pass

def begin_templating(initial_file):
    df = pd.read_excel(initial_file)
    df = bring_to_template(df)  # Bring it to initial template, delete the unneeded rows and columns
    df = merge_lat_long(df)     # Merge Lat and Long to create 'Coordinates'
    df = modify_telephone(df)   # Add the appropriate telephone number.
    df = modify_email(df)       # Add the @rci.rogers.com
    df = rename_cols(df)        # Rename the columns to dataframe
    df = remove_the_cols(df)    # Remove the unneeded columns
    # st.write(df.to_csv(index=False).encode('utf-8'))
    st.write("Templating complete")
    st.download_button("Download CSV", df.to_csv(index=False), mime='text/csv')


def main():    
    st.title("Site Directions File Templating")
    initial_file = st.file_uploader("Upload the file", type=["xlsx", 'xls'])
    st.write(initial_file)

    cap_button = st.button("Initiate templating")

    if cap_button:
        begin_templating(initial_file)

if __name__=="__main__":
   main()
