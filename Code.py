import csv

with open('titanic.csv', encoding='utf-8') as file:

    read_file = csv.DictReader(file, delimiter=';')

    my_dict = {'male': [], 'female': []}

    for items in list(read_file):
        if float(items['age']) < 18 and int(items['survived']) == 1 and items['sex'] == 'male':
            my_dict[items['sex']] = my_dict.get(items['sex'], []) + [items['name']]
        elif float(items['age']) < 18 and int(items['survived']) == 1 and items['sex'] == 'female':
            my_dict[items['sex']] = my_dict.get(items['sex'], []) + [items['name']]
    
    for key, value in my_dict.items():
        print(*value, sep='\n')