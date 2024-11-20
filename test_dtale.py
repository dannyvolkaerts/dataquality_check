
import pandas as pd
import dtale

df = pd.read_csv('titanic.csv')

if __name__ == '__main__':
      dtale.show(df, subprocess=False)
