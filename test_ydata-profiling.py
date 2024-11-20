# https://docs.profiling.ydata.ai/latest/
# https://github.com/ydataai/ydata-profiling

import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv('titanic.csv')
profile = ProfileReport(df, title="Profiling Report")
profile.to_file("my_report.html")