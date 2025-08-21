# Data Sources Documentation

This document outlines the data sources used in this project.

## 1. SpaceX REST API

- **Endpoint Used:** `https://api.spacexdata.com/v4/launches`
- **Description:** This endpoint provides a comprehensive JSON list of all historical SpaceX launches. We use this as our primary source for launch details, including payload, rocket configuration, and landing success.
- **Data Format:** JSON
- **Key Fields Used:**
  - `flight_number`: Unique identifier for each launch.
  - `name`: Mission name.
  - `date_utc`: Date and time of the launch.
  - `rocket`: Rocket ID, to link to rocket details.
  - `success`: A boolean indicating if the overall mission was a success.
  - `cores[0].landing_success`: A boolean indicating if the first stage landing was successful. This is our target variable.
  - `cores[0].reused`: Whether the core was reused.
  - `cores[0].flight`: The flight number of this specific core.
  - `payloads`: List of payload IDs.
  - `launchpad`: Launch site ID.

## 2. Wikipedia: List of Falcon 9 and Falcon Heavy launches

- **URL:** `https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches`
- **Description:** This Wikipedia page contains a series of tables listing all Falcon 9 and Falcon Heavy launches. It is used as a secondary source to cross-reference data and potentially fill in missing values from the API.
- **Data Format:** HTML tables, scraped using the `pandas.read_html()` function.
- **Key Information Used:**
  - `Flight No.`
  - `Launch site`
  - `Payload`
  - `Launch outcome`
  - `Booster landing`