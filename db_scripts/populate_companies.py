import MySQLdb

conn = MySQLdb.connect(host= "localhost",
                  user="team4",
                  passwd="team4",
                  db="sec")
x = conn.cursor()
with open("companies.txt") as f:
    for line in f:
        name = line.rstrip()
        print name
        x.execute('''INSERT INTO companies(c_name) VALUES(%s)''', (name))
        conn.commit()

conn.close()

