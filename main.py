from clientModbus import ClienteMODBUS

dbpath = "C:\\Users\\Guilherme B. Lopes\\Documents\\GitHub\\EnergyEfficiencyproject\\DB\\database1.db"

c = ClienteMODBUS('localhost', 502, dbpath=dbpath)
c.atendimento()