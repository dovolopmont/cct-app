import json
from datetime import datetime, timedelta
import time
import sys
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# list of classes
classes = ["4A" "4B","4C","4D","4E",
           "5A","5B","5C","5D","5E",
           "6A","6B","6C","6D","6E",
           "7A","7B","7C","7D","7E",
           "8A","8B","8C","8D","8E",
           "9A","9B","9C","9D","9E"]

class ClassScheduleManager:
    def __init__(self, schedule_file):
        with open(schedule_file, "r") as f:
            self.schedules = json.load(f)

    def get_today_schedule(self, class_name):
        today = datetime.now().strftime("%A")  # Get current day (e.g., "Monday")
        class_schedule = self.schedules.get(class_name, {})
        return class_schedule.get(today, [])

    def get_next_class(self, class_name):
        schedule = self.get_today_schedule(class_name)
        now = datetime.now().time()
        for class_time in schedule:
            class_time_obj = datetime.strptime(class_time, "%H:%M").time()
            if class_time_obj > now:
                return class_time_obj
        return None

    def time_until_next_class(self, class_name):
        next_class_time = self.get_next_class(class_name)
        if next_class_time:
            now = datetime.now()
            next_class_datetime = datetime.combine(now.date(), next_class_time)
            remaining_time = next_class_datetime - now
            return remaining_time
        else:
            return "No more classes today"

# Initialisations
schedule_manager = ClassScheduleManager("./templates/class_schedules_24-25.json")
@app.route("/")
def display_classes():
    class_times = []

    for class_name in classes:
        remaining_time = schedule_manager.time_until_next_class(class_name)
        if isinstance(remaining_time, timedelta):
            minutes_left = int(remaining_time.total_seconds() // 60)
            if 0 <= minutes_left <= 15:  # Only display if the class starts within recent time frame minutes
                if (class_name, minutes_left) not in class_times:
                    class_times.append((class_name, minutes_left))
                
    class_times.sort(key=lambda x: x[1])

    current_time = datetime.now().strftime("%H:%M")

    # Return as rendered HTML
    return render_template("class_schedule_web_test.html", class_times=class_times, current_time=current_time)


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug= True)
