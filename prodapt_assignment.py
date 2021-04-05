import os
import csv

'''
building static dictionary to make sure all transactions have same headers(columns).
need to update this dictionary if we found any new headers in original bank csv files.
To avoid changes in main logic its better to update this static dictionary.
'''
static_dict = {'timestamp': 'Transaction Date', 'date': 'Transaction Date', 'date_readable': 'Transaction Date',
               'type': 'Transaction Type', 'transaction': 'Transaction Type',
               'amount': 'Amount', 'amounts': 'Amount', 'euro': 'Amount',
               'cents': 'Cents',
               'from': 'From', 'From': 'From',
               'to': 'To', 'To': 'To',
               'Bank': 'Bank'
               }

# final columns in All transactions file
main_cols = ['Bank', 'Transaction Date', 'Transaction Type', 'Amount', 'From', 'To']

try:
    if os.path.exists('All_Banks_Transactions.csv'):
        print("======== Please delete All_Banks_Transactions.csv file before testing ========")
        os.remove('All_Banks_Transactions.csv')
except:
    pass

def main():
    # Main logic start here
    count = 0
    for file in os.listdir(os.getcwd()):
        if file.endswith('.csv'):
            print(file)
            all_transactions = []
            reader = csv.DictReader(open(file))
            for row in reader:
                # Adding Bank name (here file name is the bank name) to each transaction as we are merging all bank transactions
                transaction = {'Bank': file.split('.')[0]}
                for item in row:
                    try:
                        transaction.update({
                            static_dict[item]: row[item]
                        })
                    except:
                        pass

                if 'Cents' in transaction:
                    transaction['Amount'] = float(transaction['Amount']) + float(int(transaction['Cents'])/100)
                    del transaction['Cents']
                all_transactions.append(transaction)

            # for each bank appending all transactions into final file
            # If we store all banks transactions at one place and writing at once may cause memory issues
            # So that I choosed append method for each bank
            with open('All_Banks_Transactions.csv', 'a', newline='') as csvf:
                writer = csv.DictWriter(csvf, fieldnames= main_cols)
                if count == 0:
                    writer.writeheader()
                    count += 1
                writer.writerows(all_transactions)
                csvf.close()


#function_calling
main()
print("=== All Banks transactions processed ===")