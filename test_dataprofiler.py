
import json
from dataprofiler import Data, Profiler

# Load the Titanic dataset
data = Data("titanic.csv")  # Ensure the file is in the working directory
print(data.data.head(5))  # Access data directly via a compatible Pandas DataFrame

# Create a profile of the data
profile = Profiler(data)  # Calculate Statistics, Entity Recognition, etc
readable_report = profile.report(report_options={"output_format": "pretty"})
print(json.dumps(readable_report, indent=4))