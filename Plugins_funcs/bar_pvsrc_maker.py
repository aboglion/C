import csv
from datetime import datetime
import random

def get_color(value, max_value):
    proportion = value / max_value
    red = int(255 * proportion)
    green = int(255 * (1 - proportion))
    return f'rgb({red},{green},0)'

def format_date(index):
    return f"{index:02}.02.24"

csv_file_path = "./random_numbers.csv"
try:
    with open(csv_file_path, "r") as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
except FileNotFoundError:
    data = [["Date", "Value"]]

while(len(data)<31):
    data.insert(0,['00.00.00', '0'])

current_date = datetime.now().strftime("%d.%m.%y")
last_date = data[-1][0] if len(data) > 1 else None

if last_date != current_date:
    new_value = random.randint(0, 100)
    data.append([current_date, new_value])
    if len(data)>31:data=data[-31:]


    with open(csv_file_path, "w", newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)

random_numbers = [int(row[1]) for row in data[1:]]
dates = [row[0] for row in data[1:]]
max_value = max(random_numbers) if random_numbers else 1

html_output_with_updated_design = """
<!DOCTYPE html>
<html>
<head>
<style>
.bar-chart-container {
  display: flex;
  align-items: flex-end;
  height: 20vh;
  width: 100%;
  border: 1px solid #ddd;
}

.bar-container {
  display: flex;
  flex-direction: row;
  align-items: flex-end;
  border-right: 2px solid;
  margin: 0.1vw;
  width: 100%;
}

.bar {
  width: 0.3vw;
  margin-right: 0.3vw;
  border: 1px solid black;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
  position: relative;
}

.bar-value {
  position: absolute;
  bottom: 15vh;
  padding-left: 0.9vw;
  color: black;
  font-size: 2vh;
  text-decoration: underline overline rgb(255, 90, 255);
  color: yellow;
}

.bar-label {
  writing-mode: vertical-lr;
  transform: rotate(180deg);
  font-size: 2.2vh;
  height: 20vh;
}

.last-bar {
  background-color: #2ce2cf; /* רקע ירוק כבוי לאלמנט האחרון */
}
</style>
</head>
<body>

<div class="bar-chart-container">
"""

for i, (num, date) in enumerate(zip(random_numbers, dates), start=1):
    bar_height_vh = (num / max_value) * 20
    bar_color = get_color(num, max_value)
    bar_container_class = "bar-container" if i < len(random_numbers) else "bar-container last-bar"
    html_output_with_updated_design += f"""
    <div class="{bar_container_class}">
      <div class="bar" style="height:{bar_height_vh}vh; background-color: {bar_color};">
        <span class="bar-value">{num}</span>
      </div>
      <div class="bar-label">{date}</div>

    </div>"""

html_output_with_updated_design += """
</div>
</body>
</html>
"""

with open('h.html', "w") as f:
    f.write(html_output_with_updated_design)
# הקוד כעת מכיל את העיצוב החדש ולוגיקת עבודה עם קובץ CSV, כולל הפקת גרף ברים ב-HTML
# עם נתונים מעודכנים.
