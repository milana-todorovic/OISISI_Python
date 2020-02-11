import os

def findext(rootdir, *ext):
    """Pronadji fajlove sa zadatim ekstenzijama na zadatoj putanji.

    Argumenti:
        rootdir - direktorijum koji se pretrazuje.
        *ext - ekstenzije koje se traze.
    """
    retVal = []
    
    for root, dirs, files in os.walk(rootdir):
        retVal.extend([os.path.join(root, file) for file in files if os.path.splitext(file)[-1].lower() in ext])

    return retVal
    

