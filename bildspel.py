#! /usr/bin/python

# Version: 1.03
import sys
import os
import time
import traceback
from os.path import join
from optparse import OptionParser
from shutil import copy

img_extension = ['.png', '.PNG', '.jpg', '.JPG', '.jpeg']

class Options(object):
    def __init__(self):
        self.parser = OptionParser()
        self.parser.add_option("-p", "--source_path", dest="source_path", help="Path to folder to traverse", default="")
        self.parser.add_option("-e", "--dest_drive", dest="dest_drive", help="USB drive to copy files to", default="E")
        

    def parse(self, args):
        return self.parser.parse_args(args)


def export_images(source_path, dest_drive, current_files):

    nbr_parsed = 0
    
    to_copy = []
    for_textfile = [] # holds a list of all pictures with full path, for slideshow app
    
    for root, dirs, files in os.walk(source_path):
        if not files:
            continue
        #print("  Current dir: %s" % root)
        #print("  Files: %s" % files)
        for f in files:
            file_name, file_extension = os.path.splitext(f)

            if file_extension not in img_extension:
                continue
            nbr_parsed += 1

            file_fullpath = os.path.join(root, f)
            friendly_name = file_fullpath.replace(os.sep, '_')
            if friendly_name in current_files:
                continue

            to_add = (file_fullpath, friendly_name)
            print(" * Adding to usb: %s" % str(to_add))
            to_copy.append(to_add)

    nbr_to_copy = len(to_copy)
    print("Parsed %d images and going to export %d images..." % (nbr_parsed, nbr_to_copy))

    n = 0
    percent = 0
    old_percent = 0
    for file_fullpath, friendly_name in to_copy:
        dest_img_path = os.path.join(dest_drive, friendly_name)
        copy(file_fullpath, dest_img_path)
        for_textfile.append(dest_img_path)
        n += 1
        percent = int(100*float(n)/float(nbr_to_copy))
        if percent > 1 and (percent-old_percent) == 10:
            print(" %d (%d%%) images exported" % (n, percent))
            old_percent = percent

    print("Writing textfile with all images")
    textfilepath = os.path.join(dest_drive, 'all_images.txt')
    f = open(textfilepath, 'w')

    # first write all files that already is on the usb disc
    """    
    for img in current_files:
        img_path = os.path.join(dest_drive, img)
        f.write(''.join([img_path, '\n']))
    # then write all the new ones
    for img_path in for_textfile:
        f.write(''.join(img_path, '\n'))

    f.close()
    print(" * Done")
    """
    return nbr_parsed

def get_current_files_on_destination(dest_drive):

    data = []
    dirList=os.listdir(dest_drive)
    for fname in dirList:
        file_name, file_extension = os.path.splitext(fname)
        if file_extension not in img_extension:
            continue
        #print(" Alredy on USB: %s"% fname)
        data.append(fname)

    return data

def main(argv):
    options, remaining = Options().parse(argv)
    source_path = ""
    destination_drive = ""

    try:
        source_path = options.source_path
        destination_drive = options.dest_drive
    except Exception as e:
        print("Exception: %s" % str(e))
        pass

    if not source_path or not destination_drive:
        sys.exit("You must define source path and destination drive")

    print("Going to export images to USB drive.")
    print("Source path: %s" % source_path)
    print("Destination path: %s\n" % destination_drive)

    try:
        t0 = time.time()
        print("Calculating current files on usb drive...")
        current_files = get_current_files_on_destination(destination_drive)

        print("Parsing starting...\n")
        n = export_images(source_path, destination_drive, current_files)
        t1 = time.time()

        print("\nGreat success, all done! Parsing took %.2f seconds (%d/s)" % (t1-t0, n/(t1-t0)))
    except Exception as e:
        print("\nFailure! Cause: %s" % str(e))
        traceback.print_exc()


if __name__=="__main__":
    main(sys.argv)

