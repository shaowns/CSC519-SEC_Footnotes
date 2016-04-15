import MySQLdb

conn = MySQLdb.connect(host= "localhost",
                  user="team4",
                  passwd="team4",
                  db="sec")
x = conn.cursor()

r_map = {}
f_map = {}

x.execute('''select * from rules''')
rows = x.fetchall()
for row in rows:
    r_id = row[0]
    r_name = row[1]
    r_map[r_name] = r_id

x.execute('''select * from filters''')
rows = x.fetchall()
for row in rows:
    f_id = row[0]
    f_name = row[1]
    f_map[f_name] = f_id

with open("filter_rules.txt") as f:
    for line in f:
        f_name,r_names_list = line.rstrip().split("-")
        f_name = f_name.strip()
        f_id = f_map[f_name]
        r_names = r_names_list.split(",")
        r_ids = ""
        for r_name in r_names:
            r_name = r_name.strip()
            r_id = r_map[r_name]
            r_ids = r_ids + str(r_id) + ","
        r_ids = r_ids[:-1]
        x.execute('''INSERT INTO filter_rules(f_id, r_ids) VALUES(%s, %s)''', (f_id, r_ids))
        conn.commit()

conn.close()
