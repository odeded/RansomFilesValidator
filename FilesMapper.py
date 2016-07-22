import cPickle
import getopt
import md5
import os
import shutil
import sys

READ_BUFFER_SIZE = 300
def GetHashForFile(filename):
    try:
        f = open(filename, 'rb')
        buf = f.read(READ_BUFFER_SIZE)
        f.seek(0, os.SEEK_END)
        f.seek(max(-f.tell(),-READ_BUFFER_SIZE), os.SEEK_END)
        buf += f.read(READ_BUFFER_SIZE)
        f.close()
    except OSError as err:
        print("OS error: {0}".format(err))
        return
    m = md5.new(buf)
    return m.digest()


def SaveDictionaryToFile(dict, filename):
    if os.path.isfile(filename):
        shutil.copyfile(filename,filename+".old")
    output = open(filename, 'wb')
    cPickle.dump(dict, output, -1)
    output.close()


def LoadDictionaryFromFile(filename):
    if not os.path.isfile(filename):
        return {}
    output = open(filename, 'rb')
    dict = cPickle.load(output)
    output.close()
    return dict


def ScanFolder(root, dict):
    new_files = 0
    counter = 0
    os.chdir(root)
    for root, dirs, files in os.walk('.'):
        for file in files:
            counter += 1
            full_filename = os.path.join(root, file)
            hash = GetHashForFile(full_filename)
            if full_filename in dict:  # not a new file, check if wasn't changed
                if dict[full_filename] != hash:  # if file has a different hash
                    return False, "Changed file: "+full_filename
            else:   # key not in map - i.e. new file, so add it
                dict[full_filename] = hash
                new_files += 1
    if (counter < len(dict)):
        return False, "Removed {__counter} files".format(__counter=len(dict)-counter)
    return True, "Added new {} files".format(new_files)


def main(argv):
    ROOT_FOLDER = r"c:\temp"
    DICT_FILE_NAME = r"c:\RFV\RFVDict.dat"
    try:
        opts, args = getopt.getopt(argv,"hr:d:")
    except getopt.GetoptError:
        print 'run.me [-h] [-r <root_directory>] [-d <dictionary_file>]'
        print 'Version 1.0.0'
        quit()
    for opt, arg in opts:
        if opt == '-h':
            print 'run.me [-h] [-r <root_directory>] [-d <dictionary_file>]'
            print 'Version 1.0.0'
            sys.exit()
        elif opt in ("-r"):
            ROOT_FOLDER = arg
        elif opt in ("-d"):
            DICT_FILE_NAME = arg

    if not os.path.isdir(ROOT_FOLDER):
        print "No such root folder "+ROOT_FOLDER
        quit()

    dictionary = LoadDictionaryFromFile(DICT_FILE_NAME)

    all_ok, message = ScanFolder(ROOT_FOLDER,dictionary)
    if not all_ok:
        print "******************************"
    print message
    if not all_ok:
        print "******************************"

    SaveDictionaryToFile(dictionary,DICT_FILE_NAME)



if __name__ == "__main__":
    main(sys.argv[1:])