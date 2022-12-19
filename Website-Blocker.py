from datetime import datetime
import platform, os #To check OS type

ip_address = "127.0.0.1" #All Blocked website redirected to this URL

#Read websites from website_list.txt file
lists=open("website_lists.txt","r")
Website_lists = lists.readlines()
lists.close()


#Starting and end
Start_date = datetime(2022,12,13)
End_date = datetime(2022,12,14)
Today_date = datetime(datetime.now().year,datetime.now().month,datetime.now().day)

#Return the host path depending on operating system
def Host_path():
    if platform.system() == "Windows":
        hosts = r"C:/Windows/System32/drivers/etc/hosts"
    else:
        print("Unsupported OS detected.")
        exit(0)
        
    return hosts #Returns the location of hosts file

#Function of website blocker 
def Blocker():
    while True:#Loop for matching correct time
        
        #Checking the current time is between the required hours
        if Start_date <= Today_date < End_date:
            print("Working Hours! Websites have been Blocked")
            file = open(Host_path(),"r+")
            content = file.read()
            for website in Website_lists:
                if website in content:
                    pass
                else:
                    file.write(ip_address + " " + website + '\n')
            file.close()
            break
        else:
            print("Non-Working Hours! Websites have been Unblocked")
            with open(Host_path(),"r+") as file:
                content = file.readline(0)
                file.seek(0)
                for line in content:
                    if not any(website in line for website in Website):
                        file.write(line)
                file.truncate()
        break

#Main function
def main():
    if platform.system() == "Windows":
        Blocker()
    else:
        print("Incompatible OS")
        exit(0)
        
if __name__ == "__main__":
    main()
