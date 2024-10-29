import os, sys, re

video_extensions = ["mkv", "mp4", "avi"]

class Mp3(object):
    """A class used to manipulate mp3 files."""

    def printProgressBar(self, i, total):
        """
        Call in a loop to create terminal progress bar
        @params:
            i           - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
        """
        i = int(i)
        total = int(total)
        print("\r     ["+ i*"+" + (total-i)*"-" +"]",)
        #sys.stdout.write("#")
        sys.stdout.flush()

    def safeMkDir(self,dir):
        if not os.path.isdir(self.targetDir):
            os.makedirs(self.targetDir)
        if not os.path.isdir(self.targetDir):
            print("Could not create the dir '"+ self.targetDir +"' - Aborting")
            exit()

    def atoi(self, text):
        return int(text) if text.isdigit() else text
    def sort_numericaly_a_list_of_mixed_strings(self, text):
        '''
        alist.sort(key=mp3.sort_numericaly_a_list_of_mixed_strings) sorts in human order
        Taken from stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
        and nedbatchelder.com/blog/200712/human_sorting.html
        '''
        return [ self.atoi(c) for c in re.split(r'(\d+)', text) ]

    def __init__(self, sourceDir, targetDir, transcodeTo44K = False):
        """
        Call in a loop to create terminal progress bar
        @params:
            sourceDir      - Required  : The dir containing .mp3 files to be splited (Str)
            targetDir      - Required  : Output dir (Str)
            transcodeTo44K - Optional  : Whether to transcode to 44.1K, 
                                     needed by some players (Bool)
        """
        self.sourceDir = sourceDir
        self.targetDir = targetDir
        self.transcodeTo44K = transcodeTo44K
        if transcodeTo44K:
            print("    Will transcode files to 44.1K samples/sec.")
        else:
            print("    No transcoding - samples rate will be retained.")

    def convertFile(self, fileName):
        fn = os.path.join(self.sourceDir, fileName)
        q_fn = fn.replace("'", "'\\''")
        if not os.path.isfile(fn):
            print("The file '"+ fn +"' does not exist - Aborting")
            exit()

        print("\nConverting file '"+ fileName +"'")
        self.safeMkDir(self.targetDir)
        outFileName = os.path.join(self.targetDir, fileName)
   
        cmd  = "ffmpeg -v error -i '"+ q_fn +"' -vn "
        cmd += "-f wav - | lame --resample 44.1 --preset standard - '"+ outFileName  +"'"
        os.system(cmd)
        #print cmd
        

    def splitFile(self, fileName, lenghtInSeconds=15*60, fileNameOffset=1):
        """Splits the file into parts of given lenght"""
           
        fn = os.path.join(self.sourceDir, fileName)
        q_fn = fn.replace("'", "'\\''")
        if not os.path.isfile(fn):
            print("The file '"+ fn +"' does not exist - Aborting")
            exit()

        print("\nSpliting file '"+ fileName +"'")
        fileDuration = os.popen("ffmpeg -i '"+ q_fn +"' 2>&1 | grep Duration").read()
        if fileDuration=='':
            print(f'file duration for the file "{fn}" is empty - Aborting.')
            exit()
        print("'"+fileDuration+"'")
        fileDuration = fileDuration.split()[1].split(".")[0]
        print("    File duration is", fileDuration)
        h, m, s = fileDuration.split(':')
        fileDurationSeconds = int(h) * 3600 + int(m) * 60 + int(s)
        numSplited = int(fileDurationSeconds / lenghtInSeconds)
        if fileDurationSeconds >  lenghtInSeconds*numSplited:
            numSplited += 1
        print("    Will split the file to", numSplited, "parts.")
        self.safeMkDir(self.targetDir)

        print() 
        self.printProgressBar(0,numSplited),
        for i in range(numSplited):
            startSecond = lenghtInSeconds*i
            print("startSecond is", startSecond)
            outFileNum  = str(fileNameOffset + i).zfill(2)
            outFileName = os.path.join(self.targetDir, outFileNum +".mp3")
            cmd  = "ffmpeg -v error -i '"+ q_fn +"' -vn"
            if self.transcodeTo44K:
                cmd += " -ss "+ str(startSecond)
                cmd += " -t "+ str(lenghtInSeconds)
                cmd += " -f wav - | lame --resample 44.1 --preset cbr 256 - '"+ outFileName  +"'"
            else:
                cmd += " -acodec copy -ss "+ str(startSecond)
                cmd += " -t "+ str(lenghtInSeconds) +" '"+ outFileName  +"'"
            print(cmd)
            open("log.txt",'a').write(cmd+"\n")
            os.system(cmd)
            self.printProgressBar(i+1,numSplited)
        print() 
        return numSplited
