df = pd.read_html('https://de.wikipedia.org/wiki/COVID-19-Impfung_in_Deutschland', decimal=',', thousands='.')
df_impf=df[1]
# erste Impfung in Deutschland %
df_impf_1 = df_impf.iloc[18, df_impf.columns.get_level_values(1)=='erste Impfung']
# zweite Impfung in Deutschland %
df_impf_2 = df_impf.iloc[18, df_impf.columns.get_level_values(1)=='vollst. Impfung']
# Strip the string and convert it into integer
out_1=df_impf_1[1].replace(u'\xa0%', u'').replace(',','.')
out_2=df_impf_2[1].replace(u'\xa0%', u'').replace(',','.')
out_1=float(out_1)
out_2=float(out_2)
# Build JSON
{
"id":"20210404",
"BRD erste Impfung PCT": out_1
"BRD zweite Impung PCT": out_2
}
# Insert into Cosmos DB