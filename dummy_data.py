import tabledb

session = tabledb.db_session()

u = tabledb.UserBase('mrinaal', 'abcd')
session.add(u)

u = tabledb.UserBase('nikita', 'abcd')
session.add(u)

u = tabledb.UserBase('amrit', 'abcd')
session.add(u)

u = tabledb.UserBase('varun', 'abcd')
session.add(u)


session.commit()
