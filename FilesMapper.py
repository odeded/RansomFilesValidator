import os
import md5
import cPickle
import timeit

READ_BUFFER_SIZE = 300
def GetHashForFile(filename):
    try:
        f = open(filename, 'rb')
        buf = f.read(READ_BUFFER_SIZE)
        f.seek(-READ_BUFFER_SIZE, os.SEEK_END)
        buf = f.read(READ_BUFFER_SIZE)
        f.close()
    except OSError as err:
        print("OS error: {0}".format(err))
        return
    m = md5.new(buf)
    return m.digest()


def SaveDictionaryToFile(dict, filename):
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
    os.chdir(ROOT_FOLDER)
    for root, dirs, files in os.walk('.'):
        for file in files:
            full_filename = os.path.join(root, file)
            hash = GetHashForFile(full_filename)
            if full_filename in dict:  # not a new file, check if wasn't changed
                if dict[full_filename] != hash:  # if file has a different hash
                    return False, full_filename
            else:   # key not in map - i.e. new file, so add it
                dict[full_filename] = hash
                new_files += 1
    return True, new_files


ROOT_FOLDER = r"c:\temp"
DICT_FILE_NAME = r"c:\RFV\RFVDict.dat"

dictionary = LoadDictionaryFromFile(DICT_FILE_NAME)

all_ok, result = ScanFolder(ROOT_FOLDER,dictionary)
if not all_ok:
    print "******************************"
    print "Changed file - " + result
    print "******************************"
    quit()

print "Added new {} files".format(result)
SaveDictionaryToFile(dictionary,DICT_FILE_NAME)

