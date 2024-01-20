import os
import glob 
import json

# התיקייה בה נמצאים הקבצים בסיומת CVS
folder_path = "./cvss/"
output_filename = "all_cvs"
# last_price,Last_price_avg_short,Last_price_avg_medium,Last_price_avg_long,TIME
# יצירת רשימה לאחסון הנתונים המסוננים מהקבצים
filtered_data = []
files=sorted(glob.glob(folder_path+"/*.cvs"))
# last_price,Last_price_avg_short,Last_price_avg_medium,Last_price_avg_long,TIME

# מעבר על כל הקבצים בתיקייה
for file in files:
        with open(file, 'r') as csv_file:
            rows =csv_file.readlines()
            for row in rows:
                row=row.split(",")
                if len(row)>3:
                    del row[1]
                    row=",".join(row)
                    with open(output_filename, 'a+') as file_out:
                         file_out.write(row)
                    
                # מעבר על שורות הקובץ וסינון הנתונים
print("finsh")
