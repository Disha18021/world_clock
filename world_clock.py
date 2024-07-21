import streamlit as st  # type: ignore
from datetime import datetime
import pytz  # type: ignore

# Mapping of common city names to pytz time zone identifiers
city_to_timezone = {
    "New York": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Mumbai": "Asia/Kolkata",
    "Delhi": "Asia/Kolkata",
    "Los Angeles": "America/Los_Angeles",
    "Paris": "Europe/Paris",
    "Berlin": "Europe/Berlin",
    "Beijing": "Asia/Shanghai",
    "Moscow": "Europe/Moscow"
}

def get_time_for_location(location):
    try:
        # Convert common city name to pytz time zone identifier if available
        timezone = city_to_timezone.get(location, location)
        
        # Check if the timezone string is valid
        if timezone not in pytz.all_timezones:
            return f"Unknown timezone: {timezone}"
        
        timezone = pytz.timezone(timezone)
        current_time = datetime.now(timezone)
        return current_time.strftime('%Y-%m-%d %H:%M:%S')
    except pytz.UnknownTimeZoneError:
        return f"Unknown timezone: {location}"
    except Exception as e:
        return str(e)

def main():
    st.title("World Clock Agent")

    # Input box for locations
    locations = st.text_area("Enter locations (one per line):")

    if st.button("Get Date and Time"):
        if locations:
            location_list = locations.split('\n')
            location_list = [loc.strip() for loc in location_list if loc.strip()]

            st.subheader("Date and Time for each location:")
            for location in location_list:
                time_info = get_time_for_location(location)
                st.write(f"{location}: {time_info}")
        else:
            st.error("Please enter at least one location.")

if __name__ == "__main__":
    main()
