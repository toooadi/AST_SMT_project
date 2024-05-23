import os

"""
Recursively list subdirectories which contain .smt2-files.
Subdirectories which do not contain .smt2-files are not listed
"""    
def make_subdirectory_list(directoryPath, subdirs):
    added = False
    if (not os.path.exists(directoryPath)):
        raise ValueError("Direcory does not exist.")
    for filename in os.listdir(directoryPath):
        if (not added and filename.endswith(".smt2")):
            added = True
            subdirs.append(directoryPath)
        filePath = os.path.join(directoryPath, filename)
        if (os.path.isdir(filePath)):
            make_subdirectory_list(filePath, subdirs)