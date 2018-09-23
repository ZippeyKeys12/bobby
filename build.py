import json
import os
import re
import shutil
from distutils.dir_util import copy_tree

from data import ZData
from generate import ZGenerate
from preprocess import ZPreprocess
from strip import ZStript


def ZBuild(Name, Compress, Version, IniFiles):
    # Clean build destination
    print("Cleaning Build Destination: ", end="")
    BuildFolder = "dist/" + Name
    if os.path.exists(BuildFolder):
        shutil.rmtree(BuildFolder)

    # Make build destination and duplicate files
    os.makedirs(BuildFolder)
    copy_tree("src", BuildFolder)
    print("Successful")

    # Move to Build Folder
    os.chdir(BuildFolder + "/")

    # Compact ZScript
    print("Compacting ZScript")
    StartLump = "ZSCRIPT.zsc"
    FullFile = open(StartLump).read()
    FullFile = ZStript(FullFile)
    Data = ZData(FullFile, IniFiles)
    FullFile = ZPreprocess(FullFile, Data)
    FullFile = ZGenerate(FullFile, Data)
    if Compress:
        FullFile = ZStript(FullFile, True)
    if Version:
        FullFile = 'version "{}"'.format(Version) + FullFile
    os.remove("ZSCRIPT.zsc")
    with open(StartLump, "w+") as Output:
        Output.write(FullFile)
    shutil.rmtree("ZSCRIPT")
    print("Compacting ZScript: Successful")
    os.chdir("../")
    if os.path.isfile(Name + ".zip"):
        os.remove(Name + ".zip")
    ArchiveName = Name + ".pk3"
    if os.path.isfile(ArchiveName):
        os.remove(ArchiveName)

    # Compression
    if Compress:
        print("Compressing PK3 Archive: ", end="")
        shutil.make_archive(Name, "zip", Name)
        os.rename(Name + ".zip", ArchiveName)
        shutil.rmtree(Name)
        print("Successful")


if __name__ == "__main__":
    from sys import argv

    Path = argv[1]
    Name = os.path.basename(os.path.normpath(Path))

    Compress = False
    Version = None
    IniFiles = []
    for arg in argv[2:]:
        if arg.startswith("-C"):
            Compress = True
        elif arg.startswith("-V"):
            Version = float(arg[2:])
        elif arg.startswith("-I"):
            config = arg[2:]
            if config.find("[") == -1:
                IniFiles.append(config)
            else:
                IniFiles.extend(arg[3:1].split(","))
    os.chdir(Path)
    ZBuild(Name, Compress, Version, IniFiles)
