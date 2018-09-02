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

if __name__ == "__main__":
    argument_help = "Bad Argument:\n\t- Syntax: python " + sys.argv[0] + " [email/username OR file] [-log (optional - saves to file)]"
    data = {}
    log_file = ""

    if len(sys.argv) > 1:
        lookup = Lookup()

        # File
        if os.path.isfile(sys.argv[1]):
            # Enable file logging
            if len(sys.argv) > 2:
                if sys.argv[2] == "-log":
                    log_file = "result_" + str(time.time()) + ".txt"

            # Run file
            with open(sys.argv[1]) as f:
                print("Now searching...")
                for email in f:
                    email = email.replace("\n", "").replace(" ", "")
                    if email != "":
                        result = lookup.query_database(email)
                        if result:
                            for item in result:
                                # Split username and password
                                split_success = False
                                for split in [':', ';']:
                                    item_split = item.split(split)
                                    if len(item_split) > 1:
                                        split_success = True
                                        break
                                if split_success:
                                    e = item_split[0]; p = item_split[1]
                                    print(e + ":" + p)
                                    # Existing scanned email
                                    if e in data:
                                        if p not in data[e]:
                                            data[e].append(p)
                                    # Add new email
                                    else:
                                        data[e] = [p]
                                else:
                                    print("Splitting Error: couldn't split username from password")
                            
                            # Log into file
                            if log_file != "":
                                with open(log_file, 'w') as file:
                                    file.write(json.dumps(data, indent=4, sort_keys=False))
            print("Done!")
        
        # Individual Query                            
        else:
            data = lookup.query_database(sys.argv[1])
            if data: print("Password Found/s: ", data)
            else: print("No passwords found.")

    else: 
        print(argument_help) # Invalid Arguments
