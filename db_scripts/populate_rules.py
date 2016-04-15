import MySQLdb

conn = MySQLdb.connect(host= "localhost",
                  user="team4",
                  passwd="team4",
                  db="sec")
x = conn.cursor()
with open("rules.txt") as f:
    for line in f:
        name,flag = line.rstrip().split(",")
        print name
        x.execute('''INSERT INTO rules(r_name, is_flag) VALUES(%s, %s)''', (name, flag))
        conn.commit()

conn.close()

