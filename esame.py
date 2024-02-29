class ExamException(Exception):
    pass

class CSVFile:
    def __init__(self, name):
        if type(name) != str:
            raise ExamException("Il nome del file non è una stringa.")
        self.name = name

    def isDate(self, date):
        return (
            date
            and date[:4].isdigit() #verifica che sia un anno scritto correttamente
            and date[4:5] == "-" #verifica che ci sia il "-"
            and date[5:7].isdigit() #verifica che sia un mese scritto correttamente
            and int(date[5:7]) in range(1, 13) #verifica che sia un mese compreso tra 1 e 12
            and len(date) == 7
        )

    def isValue(self, value):
        return (
            value
            and value.isdigit() #verifica che sia un valore scritto correttamente
            and int(value) > 0 #verifica che sia un valore positivo
        )

class CSVTimeSeriesFile(CSVFile):    
    def get_data(self):
        try:
            test = open(self.name, "r")
            test.readline()
        except Exception as e:
            raise ExamException('Errore in apertura del file: "{}"'.format(e))

        file = open(self.name, "r")
        data = []
        for line in file:
            elements = line.split(",")
            try:
                elements[1] = elements[1].replace("\n", "")
            except:
                pass
            if self.isDate(elements[0]) and self.isValue(elements[1]):
                if data and data[-1][0] < elements[0] or not data:
                    elements[1] = int(elements[1])
                    data.append([elements[0], elements[1]])
                elif data and data[-1][0] >= elements[0]:
                    raise ExamException("Dato fuori posto o duplicato.")
                    
        file.close()
        return data

def find_min_max(time_series):
    my_dict = {}
    if len(time_series) > 0:
        year = time_series[0][0][:4]
        min = time_series[0][1]
        max = time_series[0][1]

        justChanged = True
                
        for element in time_series:
            if element[0][:4] != year:
                year = element[0][:4]
                min = element[1]
                max = element[1]
                justChanged = True
                
            if element[0][:4] == year:
                if justChanged:
                    my_dict[str(year)] = {"min": [element[0][5:7]], "max": [element[0][5:7]]}
                    justChanged = False
                
                if element[1] <= min:
                    if element[1] == min and element[0][5:7] != my_dict[str(year)]["min"][0]: 
                        my_dict[str(year)]["min"].append(element[0][5:7])
                    else: 
                        my_dict[str(year)]["min"] = [element[0][5:7]]
                        min = element[1]
                if element[1] >= max:
                    if element[1] == max and element[0][5:7] != my_dict[str(year)]["max"][0]:
                        my_dict[str(year)]["max"].append(element[0][5:7])
                    else:
                        my_dict[str(year)]["max"] = [element[0][5:7]]
                        max = element[1]

    return my_dict