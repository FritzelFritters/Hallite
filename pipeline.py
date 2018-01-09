import os

os.system("pep8 MyBot.py > pep8_report.txt")

os.system("zip MyBot.zip MyBot.py hlt\*")
os.system("python hlt_client\client.py bot -b MyBot.zip")