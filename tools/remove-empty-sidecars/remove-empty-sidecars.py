# remove-empty-sidecars.py
# Ronald L. Rivest
# September 13, 2014

""" This program will remove empty XMP sidecar files from one or more directories.
    The process of exporting photo library from Aperture caused the creation of lots
    of empty sidecar files.  This deletes those sidecar files that are empty.

    The definition as to what is an empty sidecar file may be different for other users.
    The constants here were taken from sidecar files I found after the conversion that looked empty to me.
"""

usage_string = \
"""\
    Usage: python3 remove-empty-sidecars.py [-f] dirname1 [dirname2 ...]
         where:
         -f means to force deletion the empty sidecars (really delete them;
            the default is to just list what changes *would* be made if the -f
            switch were given)
         dirname1, dirname2, ... are the top-level directories to work on
"""

import getopt
import os
import sys

# This variable defines what is meant by "empty sidecar file"
# This is what Aperture creates when there is no sidecar information.
empty_sidecar = \
"""<?xpacket begin='' id=''?>
<x:xmpmeta xmlns:x='adobe:ns:meta/' x:xmptk='XMP toolkit 2.9-9, framework 1.6'>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:iX='http://ns.adobe.com/iX/1.0/'>
<rdf:Description rdf:about='' xmlns:Iptc4xmpCore='http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/'>
</rdf:Description>
<rdf:Description rdf:about='' xmlns:photoshop='http://ns.adobe.com/photoshop/1.0/'>
</rdf:Description>
<rdf:Description rdf:about='' xmlns:dc='http://purl.org/dc/elements/1.1/'>
</rdf:Description>
<rdf:Description rdf:about='' xmlns:photomechanic='http://ns.camerabits.com/photomechanic/1.0/'>
</rdf:Description>
<rdf:Description rdf:about='' xmlns:xap='http://ns.adobe.com/xap/1.0/'>
	<xap:Rating>0</xap:Rating>
</rdf:Description>
</rdf:RDF>
</x:xmpmeta>
<?xpacket end='w'?>
"""
# print(len(empty_sidecar))
# (prints 803)
empty_sidecar2 = \
"""<?xpacket begin='' id=''?>
<x:xmpmeta xmlns:x='adobe:ns:meta/' x:xmptk='XMP toolkit 2.9-9, framework 1.6'>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:iX='http://ns.adobe.com/iX/1.0/'>
<rdf:Description rdf:about='' xmlns:Iptc4xmpCore='http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/'>
</rdf:Description>
<rdf:Description rdf:about='' xmlns:photoshop='http://ns.adobe.com/photoshop/1.0/'>
</rdf:Description>
<rdf:Description rdf:about='' xmlns:dc='http://purl.org/dc/elements/1.1/'>
	<dc:creator><rdf:Seq><rdf:li>Ronald L. Rivest</rdf:li></rdf:Seq></dc:creator>
	<dc:rights><rdf:Alt><rdf:li xml:lang='x-default'></rdf:li></rdf:Alt></dc:rights>
</rdf:Description>
<rdf:Description rdf:about='' xmlns:photomechanic='http://ns.camerabits.com/photomechanic/1.0/'>
</rdf:Description>
<rdf:Description rdf:about='' xmlns:xap='http://ns.adobe.com/xap/1.0/'>
	<xap:Rating>0</xap:Rating>
</rdf:Description>
</rdf:RDF>
</x:xmpmeta>
<?xpacket end='w'?>
"""

def main():
    """
    Read command line options and execute.
    """
    opts, dirnames = getopt.getopt(sys.argv[1:], "rf", ["help"])
    force_option = False
    for opt,val in opts:
        if opt == "-f":
            force_option = True
        elif opt in ["-h", "--help"]:
            print(usage_string)
            sys.exit()
    if force_option:
        print("Will actually delete empty sidecar files.")
    else:
        print("Will not actually delete any files, but will report what would be deleted.")
    retained_count = 0
    deleted_count = 0
    pretend_deleted_count = 0
    for dirname in dirnames:
        print("Working on folder: "+dirname)
        for root, dirs, files in os.walk(dirname):
            print("visiting: "+root)
            dirs.sort()
            # print(dirs)
            files.sort()
            # print(files)
            for file in files:
                if file.endswith(".XMP") or file.endswith(".xmp"):
                    full_filename = os.path.join(root,file)
                    file_contents = open(full_filename).read()
                    is_empty_sidecar = (file_contents == empty_sidecar) or (file_contents == empty_sidecar2)
                    if is_empty_sidecar:
                        if force_option:
                            os.remove(full_filename)
                            print("  "+file+" deleted (empty sidecar)")
                            deleted_count += 1
                        else:
                            print("  "+file+" not deleted (empty sidecar but no force option)")
                            pretend_deleted_count += 1
                    else:
                        print("  "+file+" retained (not an empty sidecar)")
                        retained_count += 1
    print("Number of sidecars deleted: "+str(deleted_count))
    print("Number of sidecars pretend-deleted: "+str(pretend_deleted_count))
    print("Number of sidecars retained: "+str(retained_count))
                        
if __name__ == "__main__":
    main()
