import csv


def getHosts(file):
    hosts = []
    with open(file) as csvFile:
        reader = csv.DictReader(csvFile)
        field = reader.fieldnames
        for row in reader:
            hosts.extend(
                [{field[i]:row[field[i]] for i in range(len(field))}])
    return hosts
