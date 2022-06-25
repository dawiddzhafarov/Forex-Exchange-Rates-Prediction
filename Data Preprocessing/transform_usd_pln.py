import csv
# script to process 1 minute data and transform it into 1 day data, calculating
# date | time | opening | high | low | close | volume
# momentum = open - close
# range = high - low
# OHLC = (opening + high + low + close) / 4
# adding cpi indexes, interest rates

def readCSV():
    with open('usd_pln_all.csv', newline='') as csvfile:
        doc = csv.reader(csvfile)
        openingSum = 0
        opening_counter = 0
        closingSum = 0
        maximumValue = 0
        minimumValue = 1000000.0
        currentDate = '2010.11.14'
        for row in doc:
            if row[0] == currentDate:
                # perform calculations
                openingSum += float(row[2])
                opening_counter += 1
                closingSum += float(row[5])
                if float(row[3]) > float(maximumValue):
                    maximumValue = float(row[3])
                if float(row[4]) < float(minimumValue):
                    minimumValue = float(row[4])
            else:
                openingMean = openingSum / opening_counter
                closingMean = closingSum / opening_counter
                momentum = openingMean - closingMean
                range = float(maximumValue) - float(minimumValue)
                ohlc = (openingMean + float(maximumValue) + float(minimumValue) + closingMean) / 4
                usa_cpi = getCPIusa(row[0][0:7])
                pol_cpi = getCPIpol(row[0][0:7])
                usa_interest = getInterestUsa(row[0][0:7])
                pol_interest = getInterestPol(row[0][0:7])

                # save row - 1 day
                with open('test.csv', 'a', newline='') as output:
                    writer = csv.writer(output)
                    writer.writerow([row[0], openingMean, maximumValue, minimumValue, closingMean, momentum, range, ohlc, usa_cpi,  pol_cpi, usa_interest, pol_interest])

                # set default values after calculating and saving results
                currentDate = row[0]
                openingSum = float(row[2])
                opening_counter = 1
                closingSum = float(row[5])
                maximumValue = row[3]
                minimumValue = row[4]


def readCPI():
    with open('cpi_usa.csv', newline='') as csvfile:
        doc = csv.reader(csvfile)

        for row in doc:
            if row[0].startswith('2'):
                print(row[1])
            else:
                print(row[0][3:])


def getCPIusa(date):
    with open('cpi_usa.csv', newline='') as csvfile:
        doc = csv.reader(csvfile)
        for row in doc:
            if row[0].startswith('2') and row[0] == date:
                return row[1]
            elif row[0][3:] == date:
                return row[1]


def getCPIpol(date):
    with open('cpi_pol.csv', newline='') as csvfile:
        doc = csv.reader(csvfile)
        for row in doc:
            if row[0].startswith('2') and row[0] == date:
                return row[1]
            elif row[0][3:] == date:
                return row[1]

def getInterestUsa(date):
    with open('interest_usa.csv') as csvfile:
        doc = csv.reader(csvfile)
        for row in doc:
            if row[0].startswith('2') and row[0] == date:
                return row[1]
            elif row[0][3:] == date:
                return row[1]

def getInterestPol(date):
    with open('interest_pol.csv') as csvfile:
        doc = csv.reader(csvfile)
        for row in doc:
            if row[0].startswith('2') and row[0] == date:
                return row[1]
            elif row[0][3:] == date:
                return row[1]

if __name__ == '__main__':
    with open('test.csv', 'a', newline='') as output:
        writer = csv.writer(output)
        writer.writerow(
            ['Date', 'Opening', 'High', 'Low', 'Closing', 'Momentum', 'Range','ohlc','usa_cpi', 'pol_cpi', 'usa_inter',
             'pol_inter'])
    readCSV()
