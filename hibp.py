import csv
import requests
import time 
import settings

# Settings
fileLocation = settings.fileLocation
resultFileLocation = settings.resultFileLocation
includeUnverifiedBreaches = settings.includeUnverifiedBreaches
apikey = settings.apikey
userAgent = settings.userAgent
printResultsVerbose = settings.printResultsVerbose

# Turn csv of emails into a deduped dict to work with
def getEmailAddressesFromCSV(csvName):
    emailAddresses = []
    
    # read csv file as a list of list
    with open(csvName, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Pass reader object to list() to get a list of lists
        # This is handy in case you want to use a csv with more columns
        list_of_rows = list(csv_reader)

    # Quick check for duplicate addresses 
    for r in list_of_rows:
        if r[0] not in emailAddresses:
            emailAddresses.append(r[0])
        else: 
            pass 

    # print(emailAddresses)
    return emailAddresses

wait = 1.3
reqUrl = 'https://haveibeenpwned.com/api/v3/breachedaccount/'
headers = {'hibp-api-key': apikey, 'user-agent': userAgent}

def makeRequest(email):
    # sleep = wait 
    # initialize the request
    check = requests.get(reqUrl+ email + '?includeUnverified=' + includeUnverifiedBreaches,
                 headers=headers)
    return check

def checkHIBP(email):
    # List to hold outcome of check
    hibpResult = [email]
    # takes wait time setting 
    sleep = wait 
    # initialize the request
    check = makeRequest(email)
    # retry if rate limited - shouldn't happen for anything over 1.3 seconds
    while str(check.status_code) == '429':
        print('Too fast, slow down! (Rate limited... will retry after ' + check.headers['Retry-After'] + ' seconds)'  ) 
        sleep = float(check.headers['Retry-After']) 
        time.sleep(sleep) 
        check = makeRequest(email)

    # for some reason the HIBP API wraps the response body in b''
    # this function strips that out
    cleanUp = lambda check: str(check).strip('b\'')
    
    # 404 indicates no breach found 
    if str(check.status_code) == '404':
        outcome = 'no breach found'
        if printResultsVerbose: print(email + ": " + outcome)
        # appends emails pwnage status
        hibpResult.append(outcome)
        # appends 0 to indiate FALSE 
        hibpResult.append(0)
        # appends 0 as null 
        hibpResult.append(0)
        time.sleep(sleep) 

    # 200 indicates a breach
    elif str(check.status_code) == '200': 
        outcome = 'breach found'
        if printResultsVerbose: print(email + ": " + outcome)
        # appened the emails pwnage status
        hibpResult.append(outcome)
        # appends 1 to indicate TRUE
        hibpResult.append(1)
        # appends body of HIPB response 
        hibpResult.append(cleanUp(check.content))
        time.sleep(sleep) 

    # something else happened... you'll need to debug this yourself
    else: 
        print(str(check.status_code))
        print("something went wrong... ")
        time.sleep(sleep) 

    return hibpResult


# Writes the output of the checks to a new csv
def writeFile(out):
    with open(resultFileLocation, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['email_address', 'search_outcome', 'breach_status', 'breach_detail'])
        writer.writerows(out)

# Process the various functions
def runChecks():
    emails = getEmailAddressesFromCSV(fileLocation)
    print('[!] Loaded ' + '\'' + fileLocation + '\'')

    print('[!] Beginning processing ' + '\'' + fileLocation + '\'' + ' against hibp api')
    print('')
    outcome = []
    for e in emails:
        # Checks for a header row in my data called 'email_address' 
        # Not necessary if you follow the instructions, but leaving it just in case ;-)
        if e != 'email_address':
            outcome.append(checkHIBP(e))
    
    print('')
    print('[!] Finished Processing ' + '\'' + fileLocation + '\'' + ' against hibp api')
    print('[!] Writing results to ' + '\'' + resultFileLocation + '\'' +  ' ... ')

    writeFile(outcome)
    print('[!] DONE ')
    
    # If you would like to use pandas to continue to analyse the file in a notebook
    # uncomment "return Outcome" and initialise the dataframe with it 
    # return outcome

if __name__ == "__main__":
    runChecks()