import tabledb

session = tabledb.db_session()

u = tabledb.UserBase('mrinaal', 'mrinaal')
session.add(u)

u = tabledb.UserBase('nikita', 'nikita')
session.add(u)

u = tabledb.UserBase('amrit', 'amrit')
session.add(u)

u = tabledb.UserBase('varun', 'varun')
session.add(u)

u = tabledb.UserBase('shrey', 'shrey')
session.add(u)

u = tabledb.UserBase('manish', 'manish')
session.add(u)

u = tabledb.UserBase('ayush', 'ayush')
session.add(u)

u = tabledb.UserBase('megha', 'megha')
session.add(u)


session.commit()
