import json


class MyAction:
    def __init__(self, date, action, price, ticker, shares):
        self.date = date
        self.action = action
        self.price = price
        self.ticker = ticker
        self.shares = shares


class MyStockAction:
    def __init__(self, date, dividend, split, stock):
        self.date = date
        self.dividend = dividend
        self.split = split
        self.stock = stock


def date_str_to_int(date_str):
    date = date_str.split()[0]
    date_string = date.replace('/', '-')
    return date_string

# a string of current hold stock and dividend for printing


def produce_output_str(hold, dividend):
    s = ''
    for entry in hold:
        s += '    - '
        s += str(hold[entry]['shares'])
        s += ' shares of '
        s += entry
        s += ' at $%.2f per share\n' % float(hold[entry]['price'])
    s += '    - $%.2f of dividend income' % float(dividend)
    return s


# Opening JSON file
f = open('input.json')

# returns input JSON sortedList[i]ect as a dictionary
input = json.load(f)

# Closing file
f.close()

actions = input['actions']
stock_actions = input['stock_actions']

# creating list to store all actions
list = []

# Iterating through the json list
for i in actions:
    list.append(MyAction(date_str_to_int(
        i['date']), i['action'], i['price'], i['ticker'], i['shares']))

for i in stock_actions:
    list.append(MyStockAction(date_str_to_int(
        i['date']), i['dividend'], i['split'], i['stock']))

# sort all the actions by date in asending order
sortedList = sorted(list, key=lambda x: x.date)

# create empty dictionary to store hold
hold = {}
dividend = 0
date_check = []

# check if actions occured in same date
for i in range(len(sortedList)-1):
    if sortedList[i].date == sortedList[i+1].date:
        date_check.insert(i, 1)
        date_check.insert(i+1, 1)
    else:
        date_check.insert(i, 0)

count = 0

for i in range(len(sortedList)):

    # check action type
    if type(sortedList[i]) is MyAction:
        # check buy or sell
        if sortedList[i].action == 'BUY':
            # if ticker doesn't exist, create an entry in hold
            if sortedList[i].ticker not in hold:
                hold[sortedList[i].ticker] = {'price': float(
                    sortedList[i].price), 'shares': int(sortedList[i].shares)}
            else:

                old_price = hold[sortedList[i].ticker]['price']
                new_price = float(sortedList[i].price)
                old_shares = hold[sortedList[i].ticker]['shares']
                new_shares = int(sortedList[i].shares)

                # update price
                hold[sortedList[i].ticker]['price'] = (
                    old_price * old_shares + new_price * new_shares) / (old_shares + new_shares)

                # update shares
                hold[sortedList[i].ticker]['shares'] += int(
                    sortedList[i].shares)
            if date_check[i] == 0:
                print('On ' + sortedList[i].date + ', you have:')
                print(produce_output_str(hold, dividend))
                print('  Transactions:')
                print('    - You bought %d shares of %s at a price of $%.2f per share'
                      % (int(sortedList[i].shares), sortedList[i].ticker, float(sortedList[i].price)))

        if sortedList[i].action == 'SELL':
            # SELL action

            # update shares
            hold[sortedList[i].ticker]['shares'] -= int(sortedList[i].shares)

            sell_price = float(sortedList[i].price)
            buy_price = hold[sortedList[i].ticker]['price']

            # calculate the profit
            profit = int(sortedList[i].shares) * (sell_price - buy_price)

            # check if still have shares after sell
            if hold[sortedList[i].ticker]['shares'] <= 0:
                # delete the ticker key
                del hold[sortedList[i].ticker]

            if date_check[i] == 0:
                print('On ' + sortedList[i].date + ', you have:')
                print(produce_output_str(hold, dividend))
                print('  Transactions:')
                if profit >= 0:
                    print('    - You sold %d shares of %s at a price of $%.2f per share for a profit of $%.2f'
                          % (int(sortedList[i].shares), sortedList[i].ticker, sell_price, profit))
                else:
                    print('    - You sold %d shares of %s at a price of $%.2f per share for a loss of $%.2f'
                          % (int(sortedList[i].shares),  sortedList[i].ticker, sell_price, profit))

        # check if multiple actions accoured on the same date
        if date_check[i] == 1:
            # first same date occure
            if count == 0:
                count += 1
                continue
            else:
                print('On ' + sortedList[i].date + ', you have:')
                print(produce_output_str(hold, dividend))
                print('  Transactions:')

                # check buy or sell which occured first
                if sortedList[i-1].action=='BUY':
                    print('    - You bought %d shares of %s at a price of $%.2f per share'
                          % (int(sortedList[i-1].shares), sortedList[i-1].ticker, float(sortedList[i-1].price)))
                else:
                    if profit >= 0:
                        print('    - You sold %d shares of %s at a price of $%.2f per share for a profit of $%.2f'
                          % (int(sortedList[i-1].shares), sortedList[i-1].ticker, sell_price, profit))
                    else:
                        print('    - You sold %d shares of %s at a price of $%.2f per share for a loss of $%.2f'
                          % (int(sortedList[i-1].shares),  sortedList[i-1].ticker, sell_price, profit))

                if sortedList[i].action=='BUY':
                    print('    - You bought %d shares of %s at a price of $%.2f per share'
                          % (int(sortedList[i].shares), sortedList[i].ticker, float(sortedList[i].price)))
                else:
                    if profit >= 0:
                        print('    - You sold %d shares of %s at a price of $%.2f per share for a profit of $%.2f'
                          % (int(sortedList[i].shares), sortedList[i].ticker, sell_price, profit))
                    else:
                        print('    - You sold %d shares of %s at a price of $%.2f per share for a loss of $%.2f'
                          % (int(sortedList[i].shares),  sortedList[i].ticker, sell_price, profit))
    else:
        # stock action
        if sortedList[i].stock not in hold:
            continue
        # check dividend
        if sortedList[i].dividend != "":
            dividend += hold[sortedList[i].stock]['shares'] * \
                float(sortedList[i].dividend)
            print('On ' + sortedList[i].date + ', you have:')
            print(produce_output_str(hold, dividend))
            print('  Transactions:')
            print('    - %s paid out $%.2f dividend per share, and you have %d shares'
                  % (sortedList[i].stock, float(sortedList[i].dividend), hold[sortedList[i].stock]['shares']))
        # check split
        elif sortedList[i].split != "":
            # update shares & price
            hold[sortedList[i].stock]['shares'] *= int(sortedList[i].split)
            hold[sortedList[i].stock]['price'] /= int(sortedList[i].split)
            print('On ' + sortedList[i].date + ', you have:')
            print(produce_output_str(hold, dividend))
            print('  Transactions:')
            print('    - %s split %d to 1, and you have %d shares'
                  % (sortedList[i].stock, int(sortedList[i].split), hold[sortedList[i].stock]['shares']))
