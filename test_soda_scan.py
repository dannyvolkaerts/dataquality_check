# Informatie voor configuration.yml:
# https://docs.soda.io/soda/connect-mssql.html
# Informatie voor checks.yaml:
# https://docs.soda.io/soda-cl/soda-cl-overview.html
# https://docs.soda.io/soda/quick-start-sodacl.html
# https://docs.soda.io/soda-cl/metrics-and-checks.html
# 
# Informatie voor volgend script:
# https://docs.soda.io/soda-library/programmatic.html#:~:text=To%20automate%20the%20search%20for,invocation%20example%20to%20extrapolate%20from.

# %%
from soda.scan import Scan
import csv
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

scan = Scan()
scan.set_data_source_name("bikestore_db")

# Add configuration YAML files
#########################
# Choose one of the following to specify data source connection configurations :
# 1) From a file
scan.add_configuration_yaml_file(file_path="configuration.yml")
# 2) Inline in the code
# For host, use cloud.soda.io for EU region; use cloud.us.soda.io for US region
# scan.add_configuration_yaml_str(
#     """
#     data_source events:
#       type: snowflake
#       host: ${SNOWFLAKE_HOST}
#       username: ${SNOWFLAKE_USERNAME}
#       password: ${SNOWFLAKE_PASSWORD}
#       database: events
#       schema: public

#     soda_cloud:
#       host: cloud.soda.io
#       api_key_id: 2e0ba0cb-your-api-key-7b
#       api_key_secret: 5wd-your-api-key-secret-aGuRg
#       scheme:
# """
# )

# Add variables
###############
scan.add_variables({"date": "2024-11-20"})


# Add check YAML files
##################
scan.add_sodacl_yaml_file("checks.yaml")
# scan.add_sodacl_yaml_file("./my_programmatic_test_scan/sodacl_file_two.yml")
# scan.add_sodacl_yaml_files("./my_scan_dir")
# scan.add_sodacl_yaml_files("./my_scan_dir/sodacl_file_three.yml")

# OR

# Define checks using SodaCL
##################
# checks = """
# checks for cities:
#     - row_count > 0
# """
# Add the checks to the scan
####################
# scan.add_sodacl_yaml_str(checks)
# OR Add the checks to scan with virtual filename identifier
# for advanced use cases such as partial/concurrent scans
####################
# scan.add_sodacl_yaml_str(
#     checks
#     file_name=f"checks-{scan_name}.yml",
# )

# Add template YAML files, if used
##################
# scan.add_template_files(template_path)

# Execute the scan
##################
scan.execute()


# Set logs to verbose mode, equivalent to CLI -V option
##################
scan.set_verbose(True)

# Set scan definition name, equivalent to CLI -s option
# The scan definition name MUST be unique to this scan, and
# not duplicated in any other programmatic scan
##################
scan.set_scan_definition_name("YOUR_SCHEDULE_NAME")

# Do not send results to Soda Cloud, equivalent to CLI -l option;
##################
# scan.set_is_local(True)

#%%
# Inspect the scan result
#########################
scan.get_scan_results()

# %%
# Get scan results
results = scan.get_scan_results()

# %%
# Write results to a CSV file
# Write the dictionary into a CSV file
with open("scan_results.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=results.keys())
    writer.writeheader()
    writer.writerow(results)

print("CSV file created successfully.")

# Prepare to write data to a CSV file
output_file = "scan_results_split.csv"
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Write a header
    writer.writerow(["Category", "Key", "Value"])  # Example: Category, Key, and Value fields

    # Write general fields
    for key, value in results.items():
        if isinstance(value, list):  # Handle lists separately
            for item in value:
                if isinstance(item, dict):  # Expand nested dictionaries into rows
                    for sub_key, sub_value in item.items():
                        writer.writerow([key, sub_key, sub_value])
                else:  # Handle other list items
                    writer.writerow([key, None, item])
        elif isinstance(value, dict):  # Expand single dictionaries into rows
            for sub_key, sub_value in value.items():
                writer.writerow([key, sub_key, sub_value])
        else:  # Handle simple key-value pairs
            writer.writerow([key, None, value])

print(f"CSV file with expanded rows created at: {output_file}")
# # Inspect the scan logs
# #######################
# scan.get_logs_text()

# # Typical log inspection
# ##################
# scan.assert_no_error_logs()
# scan.assert_no_checks_fail()

# # Advanced methods to inspect scan execution logs
# #################################################
# scan.has_error_logs()
# scan.get_error_logs_text()

# # Advanced methods to review check results details
# ########################################
# scan.get_checks_fail()
# scan.has_check_fails()
# scan.get_checks_fail_text()
# scan.assert_no_checks_warn_or_fail()
# scan.get_checks_warn_or_fail()
# scan.has_checks_warn_or_fail()
# scan.get_checks_warn_or_fail_text()
# scan.get_all_checks_text()

# %%
