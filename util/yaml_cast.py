#!/usr/bin/python3

import sys, getopt, yaml

def main(argv):
   student_number = ''
   test_name = ''
   StudentFiles_path = "//var//www//html//tsugi//mod//pythonauto//StudentFiles//"
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["sdt_num=","test_name="])
   except getopt.GetoptError:
      print ('yaml_cast.py -i <sdt_num> -o <test_name> (no file extensions)')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('yaml_cast.py -i <sdt_num> -o <test_name> (no file extensions)')
         sys.exit()
      elif opt in ("-i", "--sdt_num"):
         student_number = arg
      elif opt in ("-o", "--test_name"):
         test_name = arg
   
   params = [{'source': str(StudentFiles_path + student_number + '//main.c')}]
   target_path = "//var//www//html//tsugi//mod//pythonauto//tests//" + test_name + ".py.data//" + test_name +".yaml"
   with open(target_path, 'w') as f:
        data = yaml.dump(params, f)
   #print ('Student number is '+ student_number)
   #print ('Test name is '+ test_name)

if __name__ == "__main__":
   main(sys.argv[1:])