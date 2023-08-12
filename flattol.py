# if this was just import date, you would need to write datetime.date everytime
from datetime import datetime
from subprocess import run, DEVNULL, STDOUT
from pathlib import Path
from sys import argv, exi
# SPDX-License-Identifier: GPL-3.0-only

# TODO: Should test functions before writing anothter

# Global variables
VERSION_NUMBER="1.1.1"
OWNER="heliguy4599"
REPO="flattool"

BOLD_TXT = "\033[1m"
NORMAL_TXT = "\033[0m"
ERROR_TXT = "\033[1;31m"

COMMANDS = [
    "install",
    "uninstall",
    "purge",
    "search",
    "id",
    "run",
    "orphans",
    "version",
    "auto-update",
    "update-check",
    "help"
]

# Settings and stuff, 'as' stands for App Setting. LastUpdateCheck must be 10 digits
asFirstRun=True
asLastUpdateCheck="0000000000" # ?
asAutoCheckUpdate="false"
appID='' # TODO: Is this should global?

def main():
    april_fools()

def printerr(first_msg, *args):
    print(ERROR_TXT + f"error: " + NORMAL_TXT) 
    if len(args) > 0:
        for arg in args:
            print(f"\n{arg}")

def print_bold(string):
    print(BOLD_TXT + string + NORMAL_TXT)

def print_bold(string):
    print(ERROR_TXT + string + NORMAL_TXT)

# Haha, April Fools nerd
def april_fools():
    if datetime.now().month == 4 and datetime.now().day == 1:
        print("Haha, April 1st, get ejected")
        run(['eject'])

"""
checkForNewVersion() {
    currentTime=$(date +%s)
    if ((currentTime - asLastUpdateCheck < 3600)); then
        return 2
    fi
    sed -E -i "s/^asLastUpdateCheck=\"[0-9]{10}\"$/asLastUpdateCheck=\"${currentTime}\"/" "$(which flattool)"
    latestRelease=$(curl -s "https://api.github.com/repos/$owner/$repo/releases/latest")
    latestTag=$(echo "$latestRelease" | grep -o '"tag_name": "[^"]*' | cut -d'"' -f4 | head -n1)
    if [ "$latestTag" = "$versionNumber" ]; then
        return 0
    else
        return 1
    fi
}
"""
def check_for_new_version():
    curr_time = time.time()
    #TODO

def user_consent(prompt):
    consent = input(f"{prompt} [y|N]: ")
    if consent.lower() == "y":
        print("Continuing...")
        return 1
    elif consent.lower() == "n":
        print("Aborted!")
        return 0

def print_info():
    print(f"Version: {versionNumber}")
    if check_for_new_version():
        print(f"New Version: {latestTag}")
    print(f"Location: {Path.cwd()}")

def check_arg_len(min_len, max_len):
    if min_len < 0 or (min_len > max_len and max_len >= 0):
        printerr(f"Internal program error: checkArgLength called with improper min or max values {argv[0]}")
        exit(1)
   
    # Should remove this part, why would this function print something?
    if len(argv[1:]) < min_len or (max_len >= 0 and len(argv[1:]) > max_len):
        print_subcmd_help((argv[1]))
        exit(1)

def trash_file(file_path):
    # Note to heli: 
    # Maybe we should add print statements to indicate if operation was succesful or not
    # since we capturing both stdout and stderr. Or the question should be should we capture them at all?
    if Path(file_path).exists():
        if not run(["which", "trash-put"], stdout=DEVNULL, stderr=STDOUT).returncode:
            run(["trash-put", file_path])
            return
        elif not run(["which", "gio"], stdout=DEVNULL, stderr=STDOUT).returncode:
            run(["gio", "trash", file_path])
            return
        else:
            run(["rm", "-rf", f"{file_path}"])

def print_master_help():
    print("Usage: flattool <command>")
    print_info()
    print("Commands:")
    for cmd in COMMANDS:
        print_subcmd_help(cmd)

def print_subcmd_help(cmd):
    match cmd:
        case "install":
            print("\tinstall - usage: flattool install <app-query> <app-query> <app-query> ...\n"\
                  "\t\tcan also be ran with '-i'\n"\
                  "\t\tabout: Installs one or more flatpak apps with separate processes to avoid cancelling the queue if a name cannot be matched\n")
        case "uninstall":
            print("\tuninstall - usage: flattool uninstall <app-query> <app-query> <app-query> ...\n"\
                  "\t\taliases '-u', 'remove', 'rm'\n"\
                  "\t\tabout: Uninstalls one or more flatpak apps with separate processes to avoid cancelling the queue if a name cannot be matched\n")
        case "purge":
            print("\tpurge - usage: flattool purge <app-query>\n"\
                  "\t\taliases '-p'\n"\
                  "\t\tabout: Uninstalls a flatpak app and deletes its user data folder\n")
        case "search":
            print("\tsearch - usage: flattool search <app-query>\n"\
                  "\t\taliases '-s'\n"\
                  "\t\tabout: Searches installed flatpaks and returns lines from 'flatpak list' that match the query\n")
        case "id":
            print("\tid - usage: flattool id <app-query>\n"\
                  "\t\tabout: Returns the first matching Application ID for the query\n")
        case "run":
            print("\trun - usage: flattool run <app-query>\n"\
                  "\t\taliases '-r'\n"\
                  "\t\tabout: Runs the first matching application for the query, not requiring the full Application ID. Passes any extra arguments to the app to run except '--help' and '-h'\n")
        case "orphans":
            print("\torphans - usage: flattool orphans\n"\
                  "\t\taliases '-o'\n"\
                  "\t\tabout: Looks through ~/.var/app (the user data folder) and finds all folders that do not have corrosponding installed flatpaks, then prompts asks user what to do with them\n")
        case "version":
            print("\tversion - usage: flattool version\n"\
                  "\t\taliases '-v', '--version'\n"\
                  "\t\tabout: Prints the currently running version of flattool and where flattool is running from\n")
        case "auto-update":
            print("\tauto-update - usage: flattool auto-update\n"\
                  "\t\tabout: Toggles whether flattool will check for updates on each run\n")
        case "update-check":
            print("\tupdate-check: flattool update-check\n"\
                  "\t\tabout: Checks github to see if there is a new release and if there is, prompts to install it. Can only check once an hour.\n")
        case "help":
            print("\thelp - usage: flattool help\n"\
                  "\t\taliases '-h', '--help'\n"\
                  "\t\tabout: Prints the full help message for flattool")
        case _:
            print("Subcommand does NOT exist!")

# Main functions for the app
# ====================================================================================
def identify_by_query(query):
    app = run(["flatpak", "list"])
    if app:
        exit(1)
    return app

"""
identifyByQuery() {
    app=$(flatpak list | awk -v app="${1,,}" -F '\t' 'tolower($0) ~ app { print $2 }' | head -n 1)
    if [ -z "$app" ]; then
        printerr "No Application ID found from query: '${boldTxt}${1}${normalTxt}'"
        exit 1
    fi
    appID=$app
}
"""

"""
searchApp() {
    output=$(flatpak list | grep -i "$1")
    if [ -z "$output" ]; then
        printerr "No installed application found from query: '${boldTxt}${1}${normalTxt}'"
        exit 1
    fi
    echo "$output"
}
"""

"""
installApp() {
    # Do multiple flatpak installs for multiple apps
    while [ $# -gt 0 ]; do
        flatpak install "$1"
        echo
        shift
    done
}
"""

"""
removeApp() {
    # Do multiple flatpak removes for multiple apps
    while [ $# -gt 0 ]; do
        flatpak remove "$1"
        echo
        shift
    done
}
"""

"""
purgeApp() {
    identifyByQuery "$1"
    userConsent "Are you sure you want to uninstall ${boldTxt}${appID}${normalTxt} and delete its user data?"
    flatpak uninstall "$appID"
    trashFile "${HOME}/.var/app/${appID}"
}
"""

"""
fixOrphans() {
    echo "Checking '~/.var/app' for orphaned folders..."
    orphanedAppsList=()
    for element in "$HOME/.var/app/"*; do
        element=$(basename "$element")
        foundApp=$(flatpak list | grep -i "$element")
        if [ -z "$foundApp" ]; then
            orphanedAppsList+=( "$element" )
        fi
    done

    if [ -n "${orphanedAppsList[0]}" ]; then #check for if the first element is empty, which will indicate if there is no orphaned apps
        echo -e "\nThese user data folders exist with no installed flatpaks:"
        for element in "${orphanedAppsList[@]}"; do
            echo "  $element"
        done
        echo

        echo "What would you like to do with these folders?"
        echo "  1) Attempt to install matching flatpaks"
        echo "  2) Delete these folders"

        totalOfOrphans=${#orphanedAppsList[@]}
        maxChoices=2
        if [ "$totalOfOrphans" -gt 1 ]; then
            echo "  3) Decide for each folder individually"
            maxChoices=3
        fi

        echo -en "\nWhich option do you want to use (0 to abort)? [0-${maxChoices}]: "
        while true; do
            read -r answer
            if ! [ "$answer" -eq "$answer" ] 2>/dev/null || [ "$answer" -lt 0 ] || [ "$answer" -gt "$maxChoices" ]; then
                echo -n "Which option do you want to use (0 to abort)? [0-${maxChoices}]: "
            else
                break
            fi
        done

        case "$answer" in
            1)
                echo "Attempting to install..."
                installApp "${orphanedAppsList[@]}"
                ;;
            2)
                echo "Deleting..."
                for element in "${orphanedAppsList[@]}"; do
                    trashFile "${HOME}/.var/app/${element}"
                done
                ;;
            3)
                for element in "${orphanedAppsList[@]}"; do
                    echo "For folder '${element}', choose an option"
                    echo -n "[T]rash, [I]install, or [S]kip: "
                    while true; do
                        read -r answer
                        case "$answer" in
                            [Tt])
                                echo "Deleting..."
                                trashFile "${HOME}/.var/app/${element}"
                                break
                                ;;
                            [Ii])
                                echo "Attempting to install"
                                installApp "$element"
                                break
                                ;;
                            [Ss])
                                echo "Skipping"
                                break
                                ;;
                            *)
                                echo -n "[T]rash, [I]install, or [S]kip: "
                                ;;
                        esac
                    done
                done
                ;;
            *)
                echo "Aborted"
                ;;
        esac
    else
        echo "There are no orphaned user data folders"
    fi
}
"""
# ====================================================================================

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# <><><><><><><><><><><=[ B E G I N   M A I N   P R O G R A M ]=<><><><><><><><><><><>
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

"""
if [ "$asFirstRun" == "true" ]; then
    sed -i 's/^asFirstRun="true"$/asFirstRun="false"/' "$(which flattool)"
    echo -e "Thank you for using flattool! This is the first time its being ran. Make sure to run 'flattool --help' if you are unsure of how to use this.\n"
    echo -e "flattool can check for updates, these checks will occur on every run, so long as it has been an hour since the last check."
    echo -e "To install an update, run 'flattool update-check'."
    echo -n "Do you want to enable auto update checking? (You can change your mind later with 'flattool auto-update') [Y|n]: "
    read -r answer
    case $answer in
        [Nn])
            sed -i 's/^asAutoCheckUpdate="true"$/asAutoCheckUpdate="false"/' "$(which flattool)"
            ;;
        *)
            sed -i 's/^asAutoCheckUpdate="false"$/asAutoCheckUpdate="true"/' "$(which flattool)"
            ;;
    esac
    
    # Check which trashing methods, if any, are avaialable
    if command -v trash-put >/dev/null 2>&1; then
        echo "flattool found trash-cli on your system, nice! Any deleted data will be moved to your trash."
    else 
        if command -v gio >/dev/null 2>&1; then
            echo "flattool found gio on your system, nice! Any deleted data will be moved to your trash."
            echo "flattool also works with trash-cli, by the way."
        else
            echo "Sadly flattool found no supported method for trashing your files. And deleted data will be ${boldTxt}perminantly deleted${normalTxt}."
        fi
    fi
fi
"""

# Setting the subcommand
"""
subcommand=$1
"""

"""
if [ "$asAutoCheckUpdate" == "true" ] && [ "$subcommand" != "update-check" ] && [ "$subcommand" != "auto-update" ]; then
    checkForNewVersion
    if [ $? -eq 1 ]; then
        echo "New version of flattool is available: ${latestTag}"
    fi
fi
"""

# Check if any subcommand is provided
"""
if [ $# -eq 0 ]; then
    printerr "No command specified" "See 'flattool --help'"
    exit 1
fi
"""

# Expand flags and aliases
"""
case $subcommand in
    -h)
        subcommand="help"
        ;;
    -i)
        subcommand="install"
        ;;
    -u | rm | remove)
        subcommand="uninstall"
        ;;
    -r)
        subcommand="run"
        ;;
    -p)
        subcommand="purge"
        ;;
    -o)
        subcommand="orphans"
        ;;
    -s)
        subcommand="search"
        ;;
    -v | --version)
        subcommand="version"
        ;;
esac
"""

# Calling the correct subcommand help responses
"""
if [ "$#" -gt 0 ] && [ "${*:$#}" == "-h" ] || [ "${*:$#}" == "--help" ]; then
    if [ "$#" -eq 1 ]; then
        printMasterHelp
        exit 0
    fi
    printSubcommandHelp "$subcommand"
    exit 0
fi
"""

# Switch case to run the proper function per subcommand
"""
case "$subcommand" in
    id)
        checkArgLength 1 -1 "$@"
        shift
        while [ $# -gt 0 ]; do
            identifyByQuery "$1"
            echo "$appID"
            shift
        done
        ;;
    run)
        checkArgLength 1 -1 "$@"
        if [ "$2" = "-m" ] || [ "$2" = "--multiple" ]; then
            shift 2
            while [ $# -gt 0 ]; do
                identifyByQuery "$1"
                flatpak run "$appID" & disown
                shift
            done
            exit
        fi
        identifyByQuery "$2"
        shift 2
        flatpak run "$appID" "$@"
        ;;
    install)
        checkArgLength 1 -1 "$@"
        shift
        installApp "$@"
        ;;
    uninstall)
        checkArgLength 1 -1 "$@"
        shift
        removeApp "$@"
        ;;
    purge)
        purgeApp "$2"
        ;;
    search)
        searchApp "$2"
        ;;
    orphans)
        fixOrphans
        ;;
    help)
        printMasterHelp
        ;;
    version)
        printinfo
        ;;
    auto-update)
        if [ "$asAutoCheckUpdate" = "true" ]; then
            sed -i 's/^asAutoCheckUpdate="true"$/asAutoCheckUpdate="false"/' "$(which flattool)"
            echo "flattool will not check for updates on each run. To manually check, run 'flattool update-check'"
        else
            sed -i 's/^asAutoCheckUpdate="false"$/asAutoCheckUpdate="true"/' "$(which flattool)"
            echo "flattool will check for updates on each run."
        fi
        ;;
    update-check)
        asLastUpdateCheck="0000000000"
        checkForNewVersion
        case $? in
            0)
                echo "flattool is up to date"
                ;;
            1)
                echo "New version of flattool is available: ${latestTag}"
                userConsent "Do you want to install this new update?"
                echo "Installing new version..."
                wget -N -P "$(dirname "$(which flattool)")" "https://raw.githubusercontent.com/${owner}/${repo}/main/flattool"
                ;;
        esac
        exit 0
        ;;
    *)
        printerr "'${subcommand}' is not a flattool command" "See 'flattool --help'"
        ;;
esac
"""

if __name__ == "__main__":
    main()

