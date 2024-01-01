import json,os

def rename_re(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_name = base + str(counter) + ext
    
    while os.path.exists(new_name):
        counter += 1
        new_name = base + str(counter) + ext
        
    try:
        os.rename(filename, new_name)
        print(f"Renamed {filename} to {new_name}")
    except Exception as e:
        print(e)



def Save_data_to_file(data,data_file_name):
    try:
        if os.path.exists(data_file_name):rename_re(data_file_name)
        with open(data_file_name, 'a+') as file:
            json.dump(data, file)    
    except Exception as e:print(e)