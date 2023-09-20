#Lars Jensen
#CS 021H
#Program to take in specific stats from red sox batters in 2020 season, as well as their salary, and compute each players value
#per dollar using a formula I developed. Then will print a report on the season, including leaders. In the report it will say
#which players should be released/traded based low value. 

#import math
import math

#define main
def main():

    #ask user for filename
    filename = "reading in Red Sox 2020 Offensive Stats? "

    #call open file function
    stats_input = get_file_name(filename)

    #error handle opening file
    try:
        
        #open the file of the grades
        infile = open(stats_input, 'r')

    #say file doesn't exist if there is an issue
    except IOError:

        #print message
        print("File doesn't exist! Please run again and choose one that does.")

    #handle other possible error
    except:

        #print message
        print("Something is wrong!")

    #continue with code if everything else works
    else:

        #set number of players to zero and total k rate, kor, and ops
        players = 0
        total_k_rate = 0
        total_ops = 0
        total_kor = 0
        total_coop = 0

        #set lsit of players to be cut/traded
        tradeblock = []

        #set lowest k rate to 100
        low_k_rate = 100

        #set highest ops to 0
        high_ops = 0

        #set highest kor to 0
        high_kor = 0

        #set best value (lowest coop) to 100
        low_coop = 100

        #read first line
        line = infile.readline()

        #handle error if there is nothing in file
        if line == '':

            #print statement
            print("Error reading file, please check it isn't empty.")

        #continue if no issue
        else:

            #make sure it contains the correct data
            try:

                #create loop to keep reading
                while line != '':
                        
                    #strip new line characters
                    line = line.rstrip('\n')

                    #split into list
                    stats_list = line.split("/")

                    #Set name equal to first element
                    name = stats_list[0]

                    #set k rate to second element
                    k_rate = stats_list[1]

                    #strip the percent sign off k-rate
                    k_rate = k_rate[0:-1]

                    #set obp to thrid element
                    obp = stats_list[2]

                    #set slugging to 4th element
                    slg = stats_list[3]

                    #set salary to 5th element
                    salary = stats_list[4]

                    #strip off dollar sign
                    salary = salary[1:]

                    #remove comma
                    salary = salary.replace(",", '')

                    #convert to numbers
                    obp = float(obp)
                    slg = float(slg)
                    k_rate = float(k_rate)

                    #add 1 to players
                    players += 1

                    #calculate ops
                    ops = obp + slg

                    #add ops to total ops
                    total_ops += ops

                    #if ops is highest
                    if ops > high_ops:

                        #set high ops to new high ops
                        high_ops = ops

                        #format ops
                        ops = format(ops, '.3f')

                        #set player name to best ops
                        best_ops = name + '\t' + str(ops)

                    #add k_rate to total k rate
                    total_k_rate += k_rate
                    
                    #if k rate is lowest
                    if k_rate < low_k_rate:

                        #set k rate to new high
                        low_k_rate = k_rate

                        #format K_rate
                        k_rate = format(k_rate, '.1f')

                        #set player name to best k_rate
                        best_k_rate = name + '\t' + str(k_rate)

                    #call function to get players kor
                    kor = calulate_kor(ops, k_rate)

                    #add to total kor
                    total_kor += kor

                    #if kor is highest
                    if kor > high_kor:

                        #set new high kor
                        high_kor = kor

                        #format kor
                        kor = int(kor)

                        #set player name to best kor
                        best_kor = name + '\t' + str(kor)

                    #call fucntion to calculate coop
                    coop = calculate_coop(salary, kor)

                    #add to total coop
                    total_coop += coop

                    #if coop is the lowest
                    if coop < low_coop:

                        #set new low coop
                        low_coop = coop

                        #player name to best coop
                        best_coop = name + '\t' + str(coop)

                    #if coop is over 4 then add player to trade block
                    if coop > 4.0:

                        #add player name
                        tradeblock.append(name)

                    #read next line
                    line = infile.readline()
                    
                #close infile
                infile.close()

            #handle error
            except:

                #print error message
                print("The information in the file appears to be incorrect. Please make sure you have the right file.")

            #carry on if nothing wrong
            else:
                   
                #calculate averages
                average_k_rate = total_k_rate / players
                average_ops = total_ops / players
                average_kor = total_kor / players
                average_coop = total_coop / players

                #convert kor to int
                average_kor = int(average_kor)

                #call function to get rating of red sox average coop
                rating = coop_value(average_coop)
                        
                #set file name to this
                filename = "writing report to? "

                #call open file function
                report_file = get_file_name(filename)

                #open file in write mode
                outfile = open(report_file, 'w')

                #write title to file
                outfile.write("Red Sox 2020 Offensive Report:" + '\n' + '\n')
                outfile.write("In this report the stat KOR is used, which stands for K-adjusted\n")
                outfile.write("Offensive Rating. The stat COOP is also used, which stands for Cost\n")
                outfile.write("Of Offense Provided. These stats were created by Lars Jensen.\n\n")
                
                #write the averages
                outfile.write("Team Average K-Rate:\t" + format(average_k_rate, '.1f') + '%\n')
                outfile.write("Team Average OPS:\t" + format(average_ops, '.3f') + '\n')
                outfile.write("Team Average KOR:\t" + str(average_kor) + '\n')
                outfile.write("Team Average COOP:\t" + format(average_coop, '.2f') + '\n')
                outfile.write("COOP Rating:\t\t" + rating + '\n\n')

                #write the team leaders
                outfile.write("Lowest K-Rate on Team:\t\t" + best_k_rate + '%\n')
                outfile.write("Highest OPS on Team:\t\t" + best_ops + '\n')
                outfile.write("Offensive MVP (High KOR):\t" + best_kor + '\n\n')

                #write the players to be traded/cut
                outfile.write("Players to be traded or cut due to bad COOP (greater than 4.0):\n")

                #create for loop to write names:
                for player in tradeblock:

                    #print name
                    outfile.write(player + '\n')

                #close outfile
                outfile.close()

#define function that takes in the second half of the question and asks the user what file to open and then returns
#the file to be opened
def get_file_name(filename):

    #ask for input file name
    name_file = input("File to use for " + filename)
    
    #return names
    return name_file
    
#define function that takes in on-base percentage (obp), slugging percentage (slg), and strikeout percentage (k_rate)
#and calculates the kor value (k-adjusted offensive rating) and returns it
def calulate_kor(ops, k_rate):

    #convert to floats
    k_rate = float(k_rate)
    ops = float(ops)

    #calculate the kor
    kor = ((ops * 1000) - (k_rate ** 1.5))

    #return kor
    return kor
    
#define function that takes in the salary and kor value of a player and then calculates their cost of offense provided, or COOP
#it will then return the COOP for that player
def calculate_coop(salary, kor):

    #set salary to int
    salary = int(salary)

    #calculate coop
    coop = (math.sqrt(salary))/kor

    #return
    return coop

#define function that will take in the average coop value for the red sox and determine the teams coop value based on the
#table I created, and return the value
def coop_value(coop):

    if coop < 0.5:
        rating = "Great"
    elif coop < 2.0:
        rating = "Good"
    elif coop < 4.0:
        rating = "Average"
    else:
        rating = "Bad"

    return rating


#call main
main()

