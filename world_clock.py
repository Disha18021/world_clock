import streamlit as st # type: ignore
from datetime import datetime
import pytz # type: ignore
from langchain.llms import HuggingFaceHub # type: ignore # Updated import
from langchain.prompts import PromptTemplate # type: ignore

# Define the prompt for LangChain
prompt_template = PromptTemplate(
    input_variables=["locations"],
    template="""
    You are a helpful assistant. When given a list of locations, you will return the current date and time for each location.

    Here are the locations: {locations}
    """
)

# Initialize the Hugging Face Hub model
llm = HuggingFaceHub(
    api_token="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",  # Replace with your Hugging Face API token
    model_name="gpt2",  # Replace with the model you want to use
)

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

def generate_response(prompt_template, llm, locations):
    prompt_text = prompt_template.format(locations=locations)
    response = llm(prompt_text)
    return response

def get_time_for_location(location):
    try:
        # Convert common city name to pytz time zone identifier if available
        if location in city_to_timezone:
            location = city_to_timezone[location]
        timezone = pytz.timezone(location)
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

            # Use LangChain to process the locations
            langchain_input = ", ".join(location_list)
            try:
                response = generate_response(prompt_template, llm, langchain_input)
                st.subheader("Response from LangChain:")
                st.write(response)  # Display the response from LangChain
            except Exception as e:
                st.error(f"Error from LangChain: {e}")

            st.subheader("Date and Time for each location:")
            for location in location_list:
                time_info = get_time_for_location(location)
                st.write(f"{location}: {time_info}")
        else:
            st.error("Please enter at least one location.")

if __name__ == "__main__":
    main()
