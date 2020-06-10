import requests , sys
import requests.packages.urllib3
from bs4 import BeautifulSoup
from colorama import Fore

def GetListConent(Filename):
    try:
        Data = open(Filename , 'r')
        return Data
    except Exception:
        print(Fore.RED + "Error: Can't Open File {0}".format(Filename))
        sys.exit()

def GetRequest(Url):
    try:
        RESPONSE = requests.get(Url.rstrip('\n'), timeout=1.3 , verify=False , allow_redirects=True)
    except Exception:
        return False

    ContentToParse = RESPONSE.content
    Soup = BeautifulSoup(ContentToParse , 'html.parser')
    Found = Soup.find_all('title')

    try:
        Title = str(Found[0]);Title = Title.replace('<title>' , '');Title = Title.replace('</title>' , '')
        return Title
    except Exception:
        return 'NONE'

def GetFilename():
    try:
        Filename = sys.argv[1]
        return Filename
    except Exception:
        return False

def ListCounter(List):
    Count = 0
    for Line in List:
        Count += 1

    return Count

def Main():
    GoodList = []
    EMPTYList = []
    NOTACTIVEList = []

    Filename = GetFilename()

    if not Filename:
        print(Fore.RED + 'Error: There is no file on your command')
        sys.exit()
    else:
        pass

    DataList = GetListConent(Filename=Filename)
    for Url in DataList:
        Title = GetRequest(Url)
        if not Title:
            print(Fore.RED + "{0} == '{1}'".format(Url.rstrip('\n') , 'NOT ACTIVE!'))
            Mix_BAD = Url.rstrip('\n') + " == " + 'NOT ACTIVE' + '\n'
            NOTACTIVEList.append(Mix_BAD)
        elif Title == 'NONE':
            print(Fore.YELLOW + "{0} == '{1}'".format(Url.rstrip('\n'),'EMPTY!'))
            Mix_EMPTY = Url.rstrip('\n') + " == " + Title + '\n'
            EMPTYList.append(Mix_EMPTY)
        else:
            print(Fore.GREEN + "{0} == '{1}'".format(Url.rstrip('\n') , Title))
            Mix_GOOD = Url.rstrip('\n') + " == " + Title + '\n'
            GoodList.append(Mix_GOOD)

    BadNumber = ListCounter(NOTACTIVEList)
    GoodNumber = ListCounter(GoodList)
    EMPTYNumber = ListCounter(EMPTYList);print('\n')

    print(Fore.YELLOW + "Number Of Good Ones : {0}".format(str(GoodNumber)))
    print(Fore.YELLOW + "Number Of Bad Ones : {0}".format(str(BadNumber)))
    print(Fore.YELLOW + "Number Of EMPTY Ones : {0}".format(str(EMPTYNumber)))

    ASK = input('Wanna Save Data? (Y . N): ')
    if ASK.lower() == 'y':
        with open('output-good', 'a') as OutFile:
            for i in GoodList:
                OutFile.write(i)

        with open('output-bad', 'a') as OutFile:
            for i in NOTACTIVEList:
                OutFile.write(i)

        with open('output-empty', 'a') as OutFile:
            for i in EMPTYList:
                OutFile.write(i)

        print(Fore.GREEN + '\nAll Data Saved.')
    else:
        print(Fore.BLUE + 'OK.')
        sys.exit()

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    Main()