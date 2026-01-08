import sqlite3
import datetime
import os
def backup():
    data = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)

    origem = "db.sqlite3"
    destino = f"{backup_dir}/db_backup_{data}.sqlite3"

    # Conexões
    con = sqlite3.connect(origem)
    bkp = sqlite3.connect(destino)

    with bkp:
        con.backup(bkp)

    bkp.close()
    con.close()

    print("Backup SQLite seguro realizado com sucesso!")
