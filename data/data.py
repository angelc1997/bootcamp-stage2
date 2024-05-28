#%%
import json, re
from database import mydb


mycursor = mydb.cursor()

# read json file
with open('data_JSON.json', encoding='utf-8-sig') as f:
    data = json.load(f)
    # print(data)


# write attr to db
for attraction in data["result"]["results"]:
    # print(attraction)

   # attraction table
    add_attraction = ("INSERT INTO attractions "
                      "(name, rate, CAT, address, mrt, longitude, latitude, direction, description, memo, date) "
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    
    attraction_data = (attraction['name'], attraction['rate'], attraction['CAT'],
                       attraction['address'], attraction['MRT'], attraction['longitude'],
                       attraction['latitude'], attraction['direction'], attraction['description'],
                       attraction['MEMO_TIME'], attraction['date'])

    mycursor.execute(add_attraction, attraction_data)
    mydb.commit()


    # picture table
    attraction_id = mycursor.lastrowid

    # write url
    pattern = r'https?://[^\s]+?\.(?:png|jpg)'
    flags = re.I
    compiled_pattern = re.compile(pattern, flags)
    image_urls = compiled_pattern.findall(attraction["file"])
    
    if image_urls:
        for url in image_urls:
            add_picture = ("INSERT INTO pictures (attr_id, url) VALUES (%s, %s)")
            picture_data = (attraction_id,url)

            mycursor.execute(add_picture, picture_data)
            mydb.commit()

# close db
mycursor.close()
mydb.close()


# %%
