import os
import glob 
import shutil

# התיקייה בה נמצאים הקבצים בסיומת CVS
folder_path = "./cvss/"
# last_price,Last_price_avg_short,Last_price_avg_medium,Last_price_avg_long,TIME
# יצירת רשימה לאחסון הנתונים המסוננים מהקבצים
filtered_data = []
files=sorted(glob.glob(folder_path+"/*.cvs"))
# last_price,Last_price_avg_short,Last_price_avg_medium,Last_price_avg_long,TIME
history_dir = 'history'

# יצירת התיקייה אם היא לא קיימת
if not os.path.exists(history_dir):
    os.makedirs(history_dir)
        # מעבר על כל הקבצים בתיקייה
for file in files:
        output_filename =os.path.basename(csv_file)[:-7]+"_DAY.cvs"
        with open(file, 'r') as csv_file:
            rows =csv_file.readlines()
            for row in rows:
                row=row.split(",")
                row=",".join(row)
                with open(output_filename, 'a+') as file_out:
                        file_out.write(row)
        shutil.move(file, history_dir)

                
                # מעבר על שורות הקובץ וסינון הנתונים
print("finsh")
