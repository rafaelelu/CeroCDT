import argparse
import pandas as pd

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-f', '--file', help='Data file name', required=True)
arg_parser.add_argument('-wg', '--weekly_goal', help='Weekly exercise days required', default=4)
args = arg_parser.parse_args()
data_file_name = args.file
weekly_goal = args.weekly_goal
if not data_file_name.endswith('.csv'):
  raise Exception("File should be a csv")

df = pd.read_csv(data_file_name, parse_dates=['Date'], dayfirst=True)
df['Week_Number'] = df['Date'].dt.isocalendar().week
df['First Day of Week'] = pd.to_datetime(df['Date']) - pd.to_timedelta(df['Date'].dt.weekday, unit='D')
df_w_days_exercised = df.groupby(['Week_Number', 'First Day of Week ', 'Participant']).size().reset_index(name='Days exercised')
df_sorted_by_week_number_and_participant = df_w_days_exercised.sort_values(by=['Week_Number', 'Participant'])
df_sorted_by_week_number_and_participant['Complete (%)'] = (df_sorted_by_week_number_and_participant['Days exercised'] * 100) / weekly_goal
print(df_sorted_by_week_number_and_participant)