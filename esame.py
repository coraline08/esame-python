#classe per le eccezioni
class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    #funzione costruttore istanziata sul nome
    def __init__(self, name):
        #setto il nome del file
        self.name = name

    #uso il metodo get_data per tornare i dati del file
    def get_data(self):  

        #creo una lista dove salvare gli elementi
        time_series = []

        #apro il file con il nome scelto dall'utente 
        try:
            my_file = open(self.name, 'r')
        except:
            raise Exception('Errore nella lettura del file')
            #esco dalla funzione tornando "niente"
            return None

        #per ogni riga del mio file 
        for line in my_file:
            #separo gli elementi dalla virgola
            elements = line.split(',')
            #se non sto processando l'intestazione
            if elements[0] != 'epoch': 
                #setto il timestamp e il valore della temperatura      
                timestamp  = elements[0]
                temperature = elements[1]
                #li converto da stringa a numero, int e float rispettivamente e provo a inserire le eccezioni
                try:
                    timestamp = int(timestamp)
                #se non è possibile 
                except:#non alzo le eccezioni perché tutto deve procedere comunque senza alzare eccezioni
                    continue
                try:
                    temperature = float(temperature)
                except:#tutto deve procedere comunque senza alzare eccezioni
                    continue
                try:
                     temperature <= 0
                except:#tutto deve procedere comunque senza alzare eccezioni
                    continue
                
                #salvo gli elementi in una variabile che andrò ad appendere nella lista values
                values = [timestamp,temperature]
                time_series.append(values)
        #chiudo il file        
        my_file.close()
        #faccio l'iterazione sul range dal primo elemento della lista time_series 
        for i in range(1, len(time_series)):
            #controllo se i timestamps non sono ordinati
            if time_series[i][0]<time_series[i-1][0]:
                #alzo l'eccezione
                raise Exception("Timestamp fuori ordine")
            #e se ci sono doppioni 
            elif time_series[i][0]==time_series[i-1][0]:
                #alzo l'eccezione
                raise Exception("Timestamp già presente")
        #faccio ritornare la lista di valori [timesstamp,temperature ] (senza intestazione)
        return time_series

def daily_stats(time_series):
    
    #lista per raccogliere i risultati finali [min,max,media]
    final_list=[]

    #lista vuota per salvare i valori giornalieri allineati con il metodo epoch
    x=[]
    
    #faccio l'iterazione su tutto il range della lista time_series
    for i in range(len(time_series)):

        #quando sono all'ultima posizione della lista time_series
        if i==(len(time_series)-1):
            #aggiungo una riga di valori alla fine per terminare il ciclo for con la lunghezza giusta 
            x.append( [ time_series[0] , time_series[1] ] )

        #uso l'operazione modulo per trovare l’inizio di un giorno dato un timestamp epoch e lo salvo insieme alla sua temperatura
        epoch = time_series[i][0]
        day_start_epoch = epoch - (epoch % 86400)
        x.append( [ day_start_epoch , time_series[i][1] ] )
        
    #creo una lista per salvare le temperature con gli stessi epochs
    temperature_list=[]

    #faccio l'iterazione sul range della lista x
    for i in range(len(x)):
        #dichiaro alcune variabili per semplificare la lettura
        epoch = x[i][0]
        temperatura = x[i][1]

        #quando sono alla prima posizione della lista temperature_list
        if i==(1,len(time_series)):
            #aggiungo la temperatura alla lista temperature_list
            temperature_list.append(temperatura)
        
        #e se sono nell'intervallo [1;len-1]
        elif i in range(1,len(x)-1):

            #se l'epoch i-esimo è uguale al suo precedente
            epoch_prec = x[i-1][0]
            if epoch==epoch_prec:
                #addo la temperatura dell'epoch in posizione i-esima alla lista delle temperature
                temperature_list.append(temperatura)

            #se l'epoch i-esimo è diverso dal suo precedente 
            elif epoch!=epoch_prec:
                #calcolo min
                minimo = min(temperature_list)
                #calcolo max
                massimo = max(temperature_list)
                #calcolo media
                media = sum(temperature_list)/len(temperature_list)
                #appendo i calcoli nella final_list
                final_list.append( [ minimo, massimo, media] )
                #svuoto la lista delle temperature per ripulire il contenuto automaticamente e proseguire con il successivo
                temperature_list.clear()

    #faccio ritornare la lista finale
    return final_list

#test
try:
    time_series_file = CSVTimeSeriesFile(name='data.csv')
    time_series = time_series_file.get_data()
    #print(time_series)
    final_list=daily_stats(time_series)
    print(final_list)
except Exception as e:
    print(e)