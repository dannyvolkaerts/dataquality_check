# https://github.com/fbdesignpro/sweetviz
import sweetviz as sv
import pandas as pd

df = pd.read_csv('titanic.csv')
report = sv.analyze(df)
report.show_html('sweetviz_report.html')
