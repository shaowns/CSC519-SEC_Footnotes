import MySQLdb

conn = MySQLdb.connect(host= "localhost",
                  user="team4",
                  passwd="team4",
                  db="sec")
x = conn.cursor()
with open("anti_rules.txt") as f:
    for line in f:
        r1_name,r2_name = line.rstrip().split("-")
        r1_name = r1_name.strip()
        r2_name = r2_name.strip()
        print r1_name
        print r2_name
        r1_id = 0
        r2_id = 0
        x.execute('''select r_id from rules where r_name = %s''', (r1_name))
        rows = x.fetchall()
        for row in rows:
            r1_id = row[0]
        x.execute('''select r_id from rules where r_name = %s''', (r2_name))
        rows = x.fetchall()
        for row in rows:
            r2_id = row[0]

        x.execute('''insert into anti_rules(r1_id, r2_id) values (%s, %s)''', (r1_id, r2_id))
        
        print r1_id
        print r2_id
        conn.commit()

conn.close()

