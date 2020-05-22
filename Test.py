import Modifierv3 as m3


def test1():
    test1 = [['ZM', '4/16/20 1:32:56pm', '4/17/20', 'C', 'S', '149.00', '3.10', '1', '0.29000000000000004', '1.24',
              '4/17/20 3:51:47pm'],
             ['ZM', '4/16/20 1:32:56pm', '4/17/20', 'C', 'S', '149.00', '3.10', '1', '0.29000000000000004', '1.23',
              '4/17/20 3:51:47pm']]
    result1 = m3.orderlister(m3.dataorg("A:\\Programing\\Finance Updater\\Test 1.csv"))
    print("Test 1- closing orders before open, open order stacked closing orders not")
    print(all(elem in result1 for elem in test1))


def test2():
    test2 = [['ZM', '4/17/20 5:00:00pm', '4/17/20', 'Exercised', 'S', '135.00', '135.00', '1', '5.00 ', '', ''],
             ['IBM', '4/24/20 5:00:00pm', '4/24/20', 'Exercised', 'S', '121.00', '121.00', '1', '0.5', '', ''],
             ['IBM', '4/24/20 5:00:00pm', '4/24/20', 'Exercised', 'S', '121.00', '121.00', '1', '0.5', '', ''],
             ['IBM', '4/24/20 5:00:00pm', '4/24/20', 'Exercised', 'S', '121.00', '121.00', '1', '0.5', '', ''],
             ['IBM', '4/24/20 5:00:00pm', '4/24/20', 'Exercised', 'S', '121.00', '121.00', '1', '0.5', '', ''],
             ['IBM', '4/24/20 5:00:00pm', '4/24/20', 'Exercised', 'S', '121.00', '121.00', '1', '0.5', '', ''],
             ['IBM', '4/24/20 5:00:00pm', '4/24/20', 'Exercised', 'S', '121.00', '121.00', '1', '0.5', '', ''],
             ['IBM', '4/24/20 5:00:00pm', '4/24/20', 'Exercised', 'S', '121.00', '121.00', '1', '0.5', '', ''],
             ['IBM', '4/24/20 5:00:00pm', '4/24/20', 'Exercised', 'S', '121.00', '121.00', '1', '0.5', '', ''],
             ['IBM', '4/24/20 5:00:00pm', '4/24/20', 'Exercised', 'S', '121.00', '121.00', '1', '0.5', '', ''],
             ['IBM', '4/24/20 5:00:00pm', '4/24/20', 'Exercised', 'S', '121.00', '121.00', '1', '0.5', '', '']]
    result = m3.orderlister(m3.dataorg("A:\\Programing\\Finance Updater\\Test 2.csv"))
    print("Test 2- various exercised options properly split")
    print(all(elem in result for elem in test2))


def testZm():
    testZm = [['ZM', '4/16/20 12:02:25pm', '4/17/20', 'P', 'S', '150.00', '3.73', '1', '0.29000000000000004', '0.13',
               '4/17/20 3:53:04pm'],
              ['ZM', '4/16/20 11:52:17am', '5/01/20', 'P', 'S', '150.00', '11.65', '1', '0.31000000000000005', '10.22',
               '4/17/20 3:52:37pm'],
              ['ZM', '4/16/20 11:52:17am', '5/01/20', 'P', 'S', '150.00', '11.65', '1', '0.45000000000000007', '10.22',
               '4/17/20 3:52:37pm'],
              ['ZM', '4/16/20 12:02:25pm', '4/17/20', 'P', 'S', '150.00', '3.73', '1', '0.29000000000000004', '0.13',
               '4/17/20 3:53:04pm']]
    result = m3.orderlister(m3.dataorg("A:\\Programing\\Finance Updater\\Test Zm150.csv"))
    print("Test Zm150- 2 sets of differnt opening trades after close at the same strike")
    print(all(elem in result for elem in testZm))

if __name__ == '__main__':
    test1()
    test2()
    testZm()
