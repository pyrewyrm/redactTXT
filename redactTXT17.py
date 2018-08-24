#! python3
# A program for REDACTING text files of OSI
# ver 0.1.7

#0.1.7 Notes- This version sanitized for public release.
#0.1.6 Notes- Finalized input options code. Debug code for file operations removed. Code adjustments for
#   for code to fit in 100 character wide window (date regex excepted). Edited commenting.

#0.1.5 Notes- Output options code finalized. Removed old code for output straight to clipboard.
#   New code for checking if desired text is copied to clipboard.
#   Date class incorporated; limited function.
#   Code started for options to pull from text file. Some debugging outputs in file read/write kept.

#0.1.4 Notes- Incorporated prototyped output options code. Revised code to remove lazy_stub calls.

#0.1.3 Notes- Edited and added to existing commenting. Added keywords to list.
#   prototyping code for option to output to clipboard or to file. Began work on date
#   purge class.


import re, pyperclip
#re provides regular expressions. pyperclip provides clipboard tools.


#Lists of keywords used by purging classes
name_list = ['Organization name'] #Org names, short names, tags, abbreviations, etc go here
members_list = ['Members'] #Conventional list of member names. Case not a concern.
keywords_list = ['meeting', 'gathering', 'document(s)?', 'intel', 'confirm(ed)?', 'observation',
                 'recon', 'manifest(s)', 'cargo', 'salvage'] #Keywords you'd like removed
unit_name_list = ['Overlord', 'Long View'] #Names of operational entities
allies_srcs_list = ['Wise Chicken', 'Scaly Bartender'] #Ally references
opfor_list = ['NPC'] #Opposition references

#Option to pull from txt file or clipboard
print('Input text from clipboard or text file?')
choice = input('1- Clipboard\n2- Text file\nInput: ')
if choice == '1':
    #Ensure User has copied text to clipboard
    print('Ensure text is copied to clipboard before completing menu selections!')
    cont= input('Press y and hit ENTER to continue: ')
    if cont == 'y':
        print('Proceeding.\n')
        pass
    else:
        print('Looks like you are not ready.')#Try again
        print('\nEnsure text is copied to clipboard before completing menu selections!')
        cont= input('Press y and hit ENTER to continue: ')
        if cont == 'y':
            print('Proceeding.\n')
            pass
        else:
            print('\nLooks like you are an idiot. Going ahead w/ program anyway.\n')
    c_text = pyperclip.paste() #paste clipboard contents to program- I know, it sounds backwards.
elif choice =='2':
    #Ensure User has file in same directory
    print('Ensure source file is in this script\'s directory prior to entering name.')
    filename = input('Input source file name: ')
    with open('%s' % filename, 'r') as source_file: #takes input of name.txt and finds file in local directory
        c_text = source_file.read()
else:
    #Inform user of stupidity. Default to clipboard copy
    print('Invalid value entered. Source text copied from clipboard.')
    c_text = pyperclip.paste() #paste clipboard contents
    print('Dumbass\n') #Diagnostic output of user state



#Define Classes and Child Classes
#Base Purge Class
class purge(object):
    '''Base purge protocol for each type'''
    use_flag = False
    error_flag = False
    def __init__(self, srclist, subText, name):
        self.srclist = srclist
        self.subText = subText
        self.name = name
    def purge_text(self):   #Purge Function
        '''Main REDACTION Function'''
        if self.use_flag == True:
            for i in self.srclist:
                global c_text
                purgeRegex = re.compile(i)
                c_text = purgeRegex.sub(self.subText, c_text)
        else:
            pass
    def set_flag(self):     #method for setting usage flag
        '''Sets Flag for usage of class and controls error flag'''
        flag = input('Turn ' + self.name + ' on? y/n: ')
        if flag == 'y' or flag == 'yes':
            self.use_flag = True
            error_flag = False
        elif flag == 'n' or flag == 'no':
            error_flag = False
        else:
            print('Incorrect Response Issued. Please use y or n')
            self.error_flag = True


#Date Purge Class - LIMITED IN DATE FORMAT: MATCHES ## MON ####
class date_purge(object):
    '''Base purge protocol for each type'''
    use_flag = False
    error_flag = False
    def __init__(self, subText, name):
        self.subText = subText
        self.name = name
    def purge_text(self):   #Purge Function
        '''Main REDACTION Function'''
        global c_text
        if self.use_flag == True: 
            purgeRegex = re.compile(r'''(\d\d\s(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s\d\d\d\d)''')
            c_text = purgeRegex.sub(self.subText, c_text)
        else:
            pass
    def set_flag(self):     #method for setting usage flag
        '''Sets Flag for usage of class and controls error flag'''
        flag = input('Turn ' + self.name + ' on? y/n: ')
        if flag == 'y' or flag == 'yes':
            self.use_flag = True
            error_flag = False
        elif flag == 'n' or flag == 'no':
            error_flag = False
        else:
            print('Incorrect Response Issued. Please use y or n')
            error_flag = True    

#Child Class for objects where case sensitivity is unneeded
class case_purge(purge):
    def purge_text(self):
        '''Main REDACTION Function'''
        global c_text
        if self.use_flag == True:
            for i in self.srclist:
                purgeRegex = re.compile(i,re.IGNORECASE)    #Revised Purge to ignorecase
                c_text = purgeRegex.sub(self.subText, c_text)
        else:
            pass

#Child class for Operation ADJ NAME format of operation names. Note this remains case sensitive.
class op_purge(purge):
    def __init__(self, subText, name):
        self.subText = subText
        self.name = name
    def purge_text(self):
        '''Main REDACTION Function'''
        global c_text
        if self.use_flag == True:
            purgeRegex = re.compile(r'Operation \w+ \w+')   #Revised for Operation pattern
            c_text = purgeRegex.sub(self.subText, c_text)
        else:
            pass


#Create Purging Object Classes
organization_name = case_purge(name_list, 'ORG', 'Organization Name')
organization_members = case_purge(members_list, 'REDACTED', 'Organization Members')
intel = case_purge(keywords_list, 'CENSORED', 'Intel flag words')
op_name = op_purge('CLASSIFIED', 'Operation Names')
unit_names = purge(unit_name_list, 'REDACTED', 'organization Units')
allies_srcs = purge(allies_srcs_list, 'XXXXXX', 'Allies and Sources')
opfor = purge(opfor_list, 'XXXXX', 'Opposition Forces')
date = date_purge('DATE UNKNOWN', 'Date/Time') #CLASS is LIMITED in date matching. See Date class comments

#Options/Classes inputs for inserting other specific terms to be purged?



#Run use_flag check switching on Purge Objects via USER selected preset-option sets or custom.
print('''Use default settings below or set custom settings?
NOTICE: To flag mentions of opfor and organization, use Custom.''')
print('Internal-Officers: 1\nInternal-All: 2\nExternal-Allies: 3\nExternal-Public: 4\nCustom: 5')
flag_setting = input('Enter 1-5: ')
if flag_setting == '1':
    allies_srcs.use_flag = True
    intel.use_flag = True
    
elif flag_setting == '2':
    allies_srcs.use_flag = True
    intel.use_flag = True
    unit_names.use_flag = True
    
elif flag_setting == '3':
    allies_srcs.use_flag = True
    intel.use_flag = True
    unit_names.use_flag = True

elif flag_setting == '4':
    allies_srcs.use_flag = True
    intel.use_flag = True
    unit_names.use_flag = True
    organization_members.use_flag = True
    op_name.use_flag = True
    date.use_flag = True

elif flag_setting == '5':
    organization_name.set_flag()
    if organization_name.error_flag ==True:
        organization_name.set_flag()
    organization_members.set_flag()
    if organization_members.error_flag == True:
        organization_members.set_flag()
    intel.set_flag()
    if intel.error_flag == True:
        intel.set_flag()
    op_name.set_flag()
    if op_name.error_flag == True:
        op_name.set_flag()         
    unit_names.set_flag()
    if unit_names.error_flag == True:
        unit_names.set_flag()
    allies_srcs.set_flag()
    if allies_srcs.error_flag == True:
        allies_srcs.set_flag()
    opfor.set_flag()
    if opfor.error_flag == True:
        opfor.set_flag()
    date.set_flag()
    if date.error_flag == True:
        date.set_flag()

else:
    print('Invalid entry. Run redactTXT again.')
    #need to learn how to loop this section on input error.


#Conduct Purge on clipboard/file text in c_text

#While all classes are present in list, class is only run if
#use_flag is set True from above . Otherwise, purge_text function passes on False
organization_name.purge_text()
organization_members.purge_text()
intel.purge_text()
op_name.purge_text()
unit_names.purge_text()
allies_srcs.purge_text()
opfor.purge_text()
date.purge_text()


#Output options for passing purged text to clipboard or file
print('Output redacted text to clipboard or text file?')
choice = input('1- Clipboard\n2- Text file\nInput: ')
if choice == '1':
    pyperclip.copy(c_text) #copies program output to clipboard
elif choice =='2':
    file_name = input('Input desired file name: ')
    with open('%s.txt' % (file_name), 'w') as purged_file:
        purged_file.write(c_text)
else:
    print('Invalid value entered. Purged text dumped to clipboard.')
    pyperclip.copy(c_text) #paste back to clipboard
    print('Dumbass') #Diagnostic output of user state

    
