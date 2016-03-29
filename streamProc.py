import errno, sys, os, shutil
import dbscan, interpolate, showLinePattern, intersect
from multiprocessing import Pool
from os.path import join

def mkdirSafe(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            shutil.rmtree(path)
            os.mkdir(path)
        else:
            raise

def streamProc(folderName):
    mkdirSafe(join(folderName, "snapshot"))
    mkdirSafe(join(folderName, "clusters"))
    mkdirSafe(join(folderName, "pattern"))
    mkdirSafe(join(folderName, "img"))

    snapshotFolder = join(folderName, "snapshot")
    clusterFolder = join(folderName, "clusters")
    patternFolder = join(folderName, "pattern")
    imgFolder = join(folderName, "img")

    length = 150

    interpolate.takeSnapshot(folderName, snapshotFolder)
    dbscan.dbscan(snapshotFolder, clusterFolder)
    intersect.Intersect(clusterFolder, patternFolder, frameLength=length).intersect()
    showLinePattern.RenderPattern(patternFolder, folderName, imgFolder, "./frameImg/", frameLength=length).renderPattern()
    shutil.move(imgFolder, join("output", folderName.replace('/','')[5:]))
    shutil.rmtree(snapshotFolder)
    shutil.rmtree(clusterFolder)
    shutil.rmtree(patternFolder)


if __name__ == '__main__':
    # pool = Pool(processes = 6)
    foldersLayer0 = os.listdir("./Data")
    trajFolders = []

    print "Probing folders"
    for foldersLayer1 in foldersLayer0:
        for foldersLayer2 in os.listdir(join("./Data",foldersLayer1)):
            trajFolders.append(join("./Data/", foldersLayer1, foldersLayer2))
    print "Done"

    print "processing"
    for trajFolder in trajFolders:
        print trajFolder
        streamProc(trajFolder)
    # pool.map(streamProc, trajFolders)
    # pool.close()
    # pool.join()
    print "Done"
