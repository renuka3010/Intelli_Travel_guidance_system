import streamlit as st
import http.client
import json

# List of popular train numbers (you can expand this list)
POPULAR_TRAINS = {
    "11401": "NANDIGRAM EXP",
    "12936": "Mumbai Rajdhani Express",
    "12009": "Shatabdi Express",
    "12213": "Duronto Express",
    "12627": "Karnataka Express",
    "12431": "Rajdhani Express (Delhi to Howrah)"
}

def get_train_schedule(train_no):
    """Fetch train schedule using the IRCTC API."""
    conn = http.client.HTTPSConnection("irctc1.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "599743e675mshfe2993a9229c1a4p1eb7d4jsn85527cd1a724",  # Replace with your RapidAPI key
        'x-rapidapi-host': "irctc1.p.rapidapi.com"
    }
    try:
        conn.request("GET", f"/api/v1/getTrainScheduleV2?trainNo={train_no}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def main():
    st.title("Train Schedule 🚆")
    st.write("Find train schedules by selecting or entering a train number.")

    # Dropdown for popular train numbers
    train_options = list(POPULAR_TRAINS.keys())
    selected_train = st.selectbox(
        "Select a popular train or enter a train number below:",
        options=train_options,
        format_func=lambda x: f"{x} - {POPULAR_TRAINS[x]}"
    )

    # Input for manual train number entry
    train_no = st.text_input("Or enter a train number manually:", key="train_no")

    # Use the selected train number or the manually entered one
    train_no_to_fetch = train_no if train_no else selected_train

    if train_no_to_fetch:
        with st.spinner("Fetching train schedule..."):
            schedule = get_train_schedule(train_no_to_fetch)
            if "error" in schedule:
                st.error(f"Error fetching train schedule: {schedule['error']}")
            else:
                # Check if the API response contains valid data
                if schedule.get("status") and "data" in schedule:
                    train_data = schedule["data"]
                    st.write(f"**Train Name:** {train_data.get('train_name', 'N/A')}")
                    st.write(f"**Train Number:** {train_data.get('train_code', 'N/A')}")
                    st.write(f"**Source Station:** {train_data.get('origin', {}).get('station_name', 'N/A')}")
                    st.write(f"**Destination Station:** {train_data.get('destination', {}).get('station_name', 'N/A')}")

                    # Extract schedule stops
                    stops = train_data.get("schedule", [])
                    if stops:
                        # Create a list of dictionaries for tabular data
                        table_data = []
                        for stop in stops:
                            table_data.append({
                                "Station": stop.get("station_name", "N/A"),
                                "Arrival Time": stop.get("arrival_time", "N/A"),
                                "Departure Time": stop.get("departure_time", "N/A")
                            })
                        
                        # Display the table
                        st.write("### Train Schedule (Stops)")
                        st.table(table_data)  # Use st.table for a static table
                        # Alternatively, use st.dataframe(table_data) for an interactive table
                    else:
                        st.warning("No stop information available.")
                else:
                    st.warning("No schedule data found for this train.")

if __name__ == "__main__":
    main()