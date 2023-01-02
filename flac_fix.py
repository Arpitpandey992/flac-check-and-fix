import os
import subprocess
import sys
import argparse


parser = argparse.ArgumentParser(description='Check and Fix FLAC Files')
parser.add_argument('flac_dir', help='Flac directory path')
parser.add_argument('--quiet', '-q', action='store_true',
                    default=False, help='No output in between?')
parser.add_argument('--recursive', '-r', action='store_true',
                    default=False, help='Check subfolders as well?')
parser.add_argument('--fix', action='store_true', default=False,
                    help='Try to fix the corrupted files?')

args = parser.parse_args()
flac_dir = args.flac_dir
fix = args.fix
quiet = args.quiet
recur = args.recursive

# Check if the directory exists
if not os.path.exists(flac_dir):
    print(f"Error: directory '{flac_dir}' does not exist")
    sys.exit(1)


def Print(s, end='\n'):
    if not quiet:
        print(s, end=end, flush=True)


badFiles = 0
fixCount = 0


def checkFile(file_path):
    global badFiles, fixCount
    try:
        print(f'Checking : {os.path.basename(file_path)}', end='\r')
        result = subprocess.run(
            ['flac', '--test', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            Print(f"==> Checksum Mismatch at {file_path} <==")
            badFiles += 1
            if fix:
                Print("Attempting to Fix...", end='')
                fix_result = subprocess.run(['flac', '--verify', '--decode-through-errors', '--preserve-modtime',
                                            '-f', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # Check the return code of the 'flac' command
                if fix_result.returncode == 0:
                    # The file was fixed
                    fixCount += 1
                    Print(f"Fixed <<<======")
                else:
                    # The file could not be fixed
                    Print("Couldn't Fix XXXXXXX")
                    Print(fix_result.stderr.decode())
    except Exception as e:
        # An exception was raised while running the 'flac' command
        Print(f"{file_path}: ERROR ({e})")


if recur:
    # Iterate through all files in the FLAC directory and its subdirectories
    for root, dirs, files in os.walk(flac_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.flac'):
                checkFile(file_path)

else:
    # Iterate through the folder only
    for file in os.listdir(flac_dir):
        file_path = os.path.join(flac_dir, file)
        if file.endswith('.flac'):
            checkFile(file_path)

print('Summary : ')
print(f"Corrupted Files Count : {badFiles}")
print(f"files Fixed : {fixCount}")
