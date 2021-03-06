import os, sys
import requests
import time
import json

class Lookup:
    def __init__(self):
        self.user_agent = {'User-Agent': 'Email_Checker'}
        self.url  = "https://ghostproject.fr/search.php"

    def query_database(self, email):
        post_data = {"param":email}
        req = requests.post(self.url,headers=self.user_agent,data=post_data)
        result = req.text.split("\\n")
        if "Error" in req.text or len(result)==2:
            return False
        else:
            return result[1:-1]

class Logging:
    def __init__(self, log_file):
        self.log_file = log_file

    def save(self, data):
        # Log into file
        if self.log_file != "":
            with open(self.log_file, 'w') as file:
                file.write(json.dumps(data, indent=4, sort_keys=False))

class Main:
    def __init__(self):
        self.data = {}
        self.lookup = Lookup()
        self.logging = Logging("result_" + str(time.time()) + ".txt")

    ''' Query File '''
    def file(self, file_name, log=True):
        with open(file_name) as f:
            print("Now searching...")
            for email in f:
                email = email.replace("\n", "").replace(" ", "")
                if email != "":
                    result = self.lookup.query_database(email)
                    if result:
                        self.append(result)
                        if log:
                            self.logging.save(self.data)                
        print("Done!")

    ''' One Query '''
    def indivdual_query(self, query):
        data = self.lookup.query_database(query)
        if data: print("Password Found/s: ", data)
        else: print("No passwords found.")

    ''' Split up Username and Password '''
    def split_text(self, text):
        for split in [':', ';']:
            item_split = text.split(split)
            if len(item_split) > 1:
                return item_split
        print("Splitting Error: couldn't split username from password")
        return False

    ''' Add result to dictionary '''
    def append(self, result):
        for item in result:
            split = self.split_text(item)
            if split:
                e = split[0]; p = split[1]
                print(e + ":" + p)
                # Existing scanned email
                if e in self.data:
                    if p not in self.data[e]:
                        self.data[e].append(p)
                # Add new email
                else:
                    self.data[e] = [p]


if __name__ == "__main__":
    argument_help = "Bad Argument:\n\t- Syntax: python " + sys.argv[0] + " [email/username OR file] [-log (optional - saves to file)]"
    
    if len(sys.argv) > 1:
        main = Main()
        
        # Query each line of file
        if os.path.isfile(sys.argv[1]):
            # Enable file logging
            if len(sys.argv) > 2:
                if sys.argv[2] == "-log":
                    main.file(sys.argv)
            main.file(sys.argv[1], log=False)

        # Individual Query
        else:
            print(sys.argv[1])
            main.indivdual_query(sys.argv[1])

    else: 
        print(argument_help) # Invalid Arguments
