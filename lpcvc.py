import subprocess
import os
import requests
import LDCalc

usr_sub = "usr_sub.py"

def findScore(name):
    avgDist = LDCalc.distanceCalc("../test_data/%s/realA.txt" % (name,), "../results/usr_result.txt")

    fpOut = open("../results/usr_LDist.txt", 'w')
    fpOut.write("The error of the solution is: %f" %(avgDist))
    fpOut.close()

def testSubmission(name):
    """
    User submissions are queued then move to '~/sites/lpcv.ai/submissions/' one at a time
    """
    #clear files in ~/Documents/run_sub

    os.system('ssh pi@referee.local "rm -r ~/Documents/run_sub/*"')

    #send user submission from ~/sites/lpcv.ai/submissions/ to r_pi
    os.system("scp ../submissions/" + usr_sub + " pi@referee.local:~/Documents/run_sub/sub.py")

    #copy test video and question to r_pi
    os.system("scp -r ../test_data/%s/pi pi@referee.local:~/Documents/run_sub/test_data" % (name,))

    #step 2: start meter.py on laptop, download pi_metrics.csv through http
    #account for pcms crashing
    with open("../results/power.csv", "w") as power:
        s = requests.Session()
        r = s.get("http://10.184.20.209/")
        power.write(r.text)


    #step 4: copy answer_txt from pi
    # name of output file? Currently any .txt file
    os.system("scp pi@referee.local:~/Documents/run_sub/*.txt ../results")

    #step 5: run LDCalc
    findScore(name)





if __name__ == "__main__":
    testSubmission("video1")