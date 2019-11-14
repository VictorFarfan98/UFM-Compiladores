import sys, getopt, argparse
import os
# insert at 1, 0 is the script path (or '' in REPL)
import subprocess

"""
if len(sys.argv) == 1:
    print("")
    print("Help Menu:")
    print("Parametro -target <stage>: [scan, parse, ast, semantic, irt, codegen] ")
    print("Parametro -opt <opt_stage>: [constant, algebraic] ")
    print("Parametro -debug <stage>: [scan, parse, ast, semantic, irt, codegen] ")
    print("")
else:
    print(sys.argv)
"""

"""
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"h:t:",["help", "target="])
    except getopt.GetoptError as err:
        print("")
        print(str(err))
        print("")
        print("Help Menu:")
        print("Parametro -target <stage>:    [scan, parse, ast, semantic, irt, codegen] ")
        print("Parametro -opt <opt_stage>:    [constant, algebraic] ")
        print("Parametro -debug <stage>:    [scan, parse, ast, semantic, irt, codegen] ")
        print("")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("")
            print("Help Menu:")
            print("Parametro -target <stage>:    [scan, parse, ast, semantic, irt, codegen] ")
            print("Parametro -opt <opt_stage>:    [constant, algebraic] ")
            print("Parametro -debug <stage>:    [scan, parse, ast, semantic, irt, codegen] ")
            print("")
            
        elif opt in ("-target"):
            inputfile = arg

        
    print(opts, args)

if __name__ == "__main__":
    main(sys.argv[1:])
"""
    


ap = argparse.ArgumentParser()
ap.add_argument("file", help="Inputfile")

ap.add_argument("-target", required=False,
    help="<stage>: [scan, parse, ast, semantic, irt, codegen]")
ap.add_argument("-opt", required=False,
    help="<opt_stage>: [constant, algebraic] ")
ap.add_argument("-debug", required=False,
    help="<stage>: [scan, parse, ast, semantic, irt, codegen] ")
args = vars(ap.parse_args())

print(args)
if args["target"] == None:
    args["target"] = "scan"


if args["target"] == "scan":    
    if args["debug"] == None:
        subprocess.call(["python", "Scanner.py", args["file"]], cwd="scanner")
    elif args["debug"] == "scan":
        subprocess.call(["python", "Scanner.py", args["file"], "-debug",args["debug"]], cwd="scanner")
    else:
        print("")
        print("Bad argument for flag -debug")
        print("")
        print("Help Menu:")
        print("Parametro -target <stage>: [scan, parse, ast, semantic, irt, codegen] ")
        print("Parametro -opt <opt_stage>: [constant, algebraic] ")
        print("Parametro -debug <stage>: [scan, parse, ast, semantic, irt, codegen] ")
        print("")
elif args["target"] == "parse":
    if args["debug"] != None:
        print("")
        print("debug argument not accepted for -target scan")
        print()
    else:
        subprocess.call(["python", "Scanner.py", args["file"]], cwd="scanner")
        subprocess.call(["python", "Parser.py", ], cwd="parser")
elif args["target"] == "semantic":
    if args["debug"] != None:
        print("")
        print("debug argument not accepted for -target scan")
        print()
    else:
        subprocess.call(["python", "Scanner.py", args["file"]], cwd="scanner")             
        subprocess.call(["python", "Semantic.py", ], cwd="semantic check")     
elif args["target"] == "irt":
    if args["debug"] != None:
        print("")
        print("debug argument not accepted for -target irt")
        print()
    else:
        subprocess.call(["python", "Scanner.py", args["file"]], cwd="scanner")             
        subprocess.call(["python", "Semantic.py", ], cwd="semantic check")    
        subprocess.call(["python", "irt.py", ], cwd="irt")

else:
    print("")
    print("Bad argument for flag -target")
    print("")
    print("Help Menu:")
    print("Parametro -target <stage>: [scan, parse, ast, semantic, irt, codegen] ")
    print("Parametro -opt <opt_stage>: [constant, algebraic] ")
    print("Parametro -debug <stage>: [scan, parse, ast, semantic, irt, codegen] ")
    print("")
