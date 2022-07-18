from cs50 import get_int, get_string
import os
clear = lambda: os.system('cls')


start_year = 1

def main():
    year = get_int(f"Enter Year for Ethiopian Calendar(start from {start_year}): ")
    month = 1
    if year < start_year:
        print(f"Invalid input")
        return(1)

    while True:
        print_calendar(month, year)#print the calendar
        #ask the user if they want to continue and store answer

        
        if month == 13:
            if  Continue(year) == 0:
                clear()#clear the console
                return(1)
            year = year + 1
            month = 1
            continue
        month = Continue(month)
        clear()#clear the console



def print_calendar(month,year):
    print(f"Month = {month}, {year}")
    print("="*35, end ="")
    print("\nMon  Tue  Wed  Thu  Fri  Sat  Sun")
    print("="*35, end ="")
    print_days(month,year)

def print_days(month,year):
    spaces = meskerem1(month,year)
    day = 1
    row = 6
    val = 30
    print("")
    if month == 13:
        row = 3
        val = pagume(year)
    for i in range(0,row,1):

        #handle the first row
        if i == 0:
            if spaces== 7:
                continue
            print("     "*int(spaces), end="")
            if (day > val):#If day is greater than val don't do anything
                continue
            for j in range(0,int(7 - spaces),1):
                print(f"{day}    ", end ="")#print the days
                day = day + 1
            print("")
            continue

        #handle the rest of the rows
        
        for a in range(0,7,1):
            if (day > val):#If day is greater than val don't do anything
                continue
            if (day < 10):
                print(f"{day}    ", end ="")#print the days
            else:
                print(f"{day}   ", end ="")#print the days
            day = day + 1
        print("")
def meskerem1(month,year):
    
    inqutatash = ((((5*year) - zemen(year)) %28) /4) + 1
    
    if month == 1:
        return inqutatash%7
    return ((inqutatash%7) +(2 * (month - 1)))% 7
def pagume(year):

    days = 5
    if zemen(year) == 3:
        days = 6 #if the year is a "Zemene Lukas" pagume has 6 days
    elif year%600 == 500:
        days =7 #if the remainder of year when divided by 600 is 500 pagume has 7 days
    
    return days
 

def Continue(now):
    
    if get_string(f"continue to {now + 1}(y/n): ") == "y":
        now = now+ 1
        return(now)
    return(0)

    # if get_string(f"continue to next {now + 1}(y/n): ") == "y":
    #     month = 1
    #     year = year+ 1
    #     return(year)
    # return(1)
def zemen(year):
    return year%4
main()  