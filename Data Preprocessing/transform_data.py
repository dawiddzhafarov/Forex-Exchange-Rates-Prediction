import csv
import string
from dataclasses import dataclass


# script to process 1-minute data and transform it into 1-day data, calculating:
# date | time | opening | high | low | close | volume
# momentum = open - close
# range = high - low
# OHLC = (opening + high + low + close) / 4
# adding cpi indexes, interest rates if specified in main func

def processCSV(source_file, output_file, start_date, with_info, filenames):
    with open(source_file, newline='') as csvfile:
        doc = csv.reader(csvfile)
        opening_sum = 0
        opening_counter = 0
        closing_sum = 0
        maximum_value = 0
        minimum_value = 1000000.0
        current_date = start_date
        for row in doc:
            if row[0] == current_date:
                # perform calculations
                opening_sum += float(row[2])
                opening_counter += 1
                closing_sum += float(row[5])
                if float(row[3]) > float(maximum_value):
                    maximum_value = float(row[3])
                if float(row[4]) < float(minimum_value):
                    minimum_value = float(row[4])
            else:
                opening_mean = opening_sum / opening_counter
                closing_mean = closing_sum / opening_counter
                momentum = opening_mean - closing_mean
                exchange_range = float(maximum_value) - float(minimum_value)
                ohlc = (opening_mean + float(maximum_value) + float(minimum_value) + closing_mean) / 4
                if with_info:
                    cpi_1 = getCPI(filenames.cpi_1, row[0][0:7])
                    cpi_2 = getCPI(filenames.cpi_2, row[0][0:7])
                    interest_1 = getInterest(filenames.interest_1, row[0][0:7])
                    interest_2 = getInterest(filenames.interest_2, row[0][0:7])

                    # save row - 1 day
                    with open(output_file, 'a', newline='') as output:
                        writer = csv.writer(output)
                        writer.writerow(
                            [row[0], opening_mean, maximum_value, minimum_value, closing_mean, momentum, exchange_range,
                             ohlc,
                             cpi_1,
                             cpi_2, interest_1, interest_2])
                else:
                    with open(output_file, 'a', newline='') as output:
                        writer = csv.writer(output)
                        writer.writerow(
                            [row[0], opening_mean, maximum_value, minimum_value, closing_mean, momentum, exchange_range,
                             ohlc])

                # set default values after calculating and saving results
                current_date = row[0]
                opening_sum = float(row[2])
                opening_counter = 1
                closing_sum = float(row[5])
                maximum_value = row[3]
                minimum_value = row[4]


def readCPI():
    with open('cpi_usa.csv', newline='') as csvfile:
        doc = csv.reader(csvfile)

        for row in doc:
            if row[0].startswith('2'):
                print(row[1])
            else:
                print(row[0][3:])


def getCPI(name, date):
    with open(name, newline='') as csvfile:
        doc = csv.reader(csvfile)

        for row in doc:
            if row[0].startswith('2') and row[0] == date:
                return row[1]
            elif row[0][3:] == date:
                return row[1]


def getInterest(name, date):
    with open(name) as csvfile:
        doc = csv.reader(csvfile)

        for row in doc:
            if row[0].startswith('2') and row[0] == date:
                return row[1]
            elif row[0][3:] == date:
                return row[1]


@dataclass
class AdditionalFiles:
    interest_1: string
    interest_2: string
    cpi_1: string
    cpi_2: string


if __name__ == '__main__':
    withAdditionalInfo = True
    outputFileName = 'test6.csv'
    sourceFileName = 'usd_pln_all.csv'
    startDate = '2010.11.14'
    interestRateFileName_1 = 'interest_pol.csv'
    interestRateFileName_2 = 'interest_usa.csv'
    CPIFileName_1 = 'cpi_pol.csv'
    CPIFileName_2 = 'cpi_usa.csv'
    addFiles = AdditionalFiles(interestRateFileName_1, interestRateFileName_2, CPIFileName_1, CPIFileName_2)

    # write header
    with open(outputFileName, 'a', newline='') as output:
        writer = csv.writer(output)
        writer.writerow(
            ['Date', 'Opening', 'High', 'Low', 'Closing', 'Momentum', 'Range', 'ohlc', 'usa_cpi', 'pol_cpi',
             'usa_inter',
             'pol_inter'])

    # process data
    processCSV(sourceFileName, outputFileName, startDate, withAdditionalInfo, addFiles)
