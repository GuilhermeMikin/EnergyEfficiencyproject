from clientModbus import ClienteMODBUS

dbpath = "C:\\Users\\Guilherme B. Lopes\\Documents\\GitHub\\EnergyEfficiencyproject\\DB\\database1.db"

c = ClienteMODBUS('127.0.0.1', 502, dbpath=dbpath)
c.atendimento()