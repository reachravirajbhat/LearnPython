import sqlite3

conn = sqlite3.connect('orgemaildb.sqlite')
cur  = conn.cursor()

# If a table names <Counts> already exists, clean up its content and delete it
cur.execute('DROP TABLE IF EXISTS Counts')

# Creat a new table named <Counts> with two fields <org> and <count>
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

# Get text file name to source data to populate <Counts> table
fname = input('Enter source file name: ')
if (len(fname) < 1): fname = 'mbox.txt'
fh = open(fname)

# Traverse every line in the file to get email id
for line in fh:
    if not line.startswith('From: '): continue

    # Split the line into words separated by space to get the email id.
    pieces  = line.split()
    email   = pieces[1]

    # Split email id into two pieces to get username and org name separated
    # by '@'
    pieces  = email.split('@')
    org     = pieces[1]

    # Search <Counts> table to see if there is already and entry with
    # org name.
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    if row is None:
        # No entry with this org name exists. Add a new one
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        # Entry exists; Increment the count for the entry by one
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
