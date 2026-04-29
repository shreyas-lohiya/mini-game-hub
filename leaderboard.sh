#!/bin/bash

#clears the terminal so that it leaderboard heading comes on top
clear

printf "\033[32m" #green

#prints heading
cat << 'EOF'

██╗     ███████╗ █████╗ ██████╗ ███████╗██████╗ ██████╗  ██████╗  █████╗ ██████╗ ██████╗ 
██║     ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
██║     █████╗  ███████║██║  ██║█████╗  ██████╔╝██████╔╝██║   ██║███████║██████╔╝██║  ██║
██║     ██╔══╝  ██╔══██║██║  ██║██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
███████╗███████╗██║  ██║██████╔╝███████╗██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 

EOF

#string to store game names as space seperated
games="Tic-Tac-Toe Othello Connect4 Chain-Reaction"

#metric option by which leaderboard is sorted and corresponding sort_option which is used as a flag in sort later
metric=$1 
[[ $metric == "Username" ]] && sort_option="-k1,1"
[[ $metric == "Wins" ]] && sort_option="-n -k2,2r -k4,4 -k3,3"
[[ $metric == "Win percent" ]] && sort_option="-k5,5r -k7,7"
[[ $metric == "Losses" ]] && sort_option="-n -k4,4r -k2,2 -k3,3r"
[[ $metric == "Loss percent" ]] && sort_option="-k7,7r -k5,5"
[[ $metric == "Wins/Losses" ]] && sort_option="-g -k8,8r -k2,2 -k3,3"

#looping over each game to display individual data
for game in $games "All Games Combined"; do
    #prints game name as a heading
    printf "\033[1;35m\n${game^^}\n\n\033[0m"

    #first awk script generates a csv data of the username,wins,draws,...
    #then sort using sort_option
    #then append heading on the csv data 
    #then column command is used to output a "║" seperated table 
    #finally last awk scripts adds horizontal lines to the table and vertical lines on the ends
    awk -v game="$game" '
    BEGIN {
        FS=","
        OFS=","
        #set game to empty string so that it matches all $4 in regex matching later
        game=(game=="All Games Combined"?"":game)
    }

    #$5 is a boolean which stores is it draw, then array data stores wins,loss,draw of each user
    $4 ~ game && $5=="False" {
        data[$1]["win"]++
        data[$2]["loss"]++
    }
    $4 ~ game && $5=="True" {
        data[$1]["draw"]++
        data[$2]["draw"]++
    }

    #after calculating each value it generates csv
    END {
        for(i in data){
            win_p=100*(data[i]["win"]+0)/(data[i]["win"]+data[i]["draw"]+data[i]["loss"])
            draw_p=100*(data[i]["draw"]+0)/(data[i]["win"]+data[i]["draw"]+data[i]["loss"])
            loss_p=100*(data[i]["loss"]+0)/(data[i]["win"]+data[i]["draw"]+data[i]["loss"])
            wbyl=(data[i]["loss"]+0 == 0) ? "inf" : (data[i]["win"]+0)/(data[i]["loss"]+0)
            printf "%s,%d,%d,%d,%8.4f,%8.4f,%8.4f,%s,\n", i,data[i]["win"]+0,data[i]["draw"]+0,data[i]["loss"]+0,win_p,draw_p,loss_p,wbyl
        }
    }
    ' history.csv | sort -t ',' $sort_option | (echo "Username,Wins,Draws,Losses,Win%,Draw%,Loss%,Wins/Losses,"; cat -;) | column -t -s "," -o "   ║ " | awk -F"║" '
    NR==1 {
        #arr stores the indices where there are line joinings
        temp=0
        for(i=1;i<=NF;i++){
            temp+=length($i)+1
            arr[temp]
        }
        
        #line above header
        printf "\033[34m╔"
        for (i=0;i<length-1;i++) {
            if (i in arr) printf "╦"
            else printf "═"
        }
        printf"╗"
        print ""

        #prints a line(header)
        printf "║ "
        for (i=1;i<NF;i++) {
            printf "\033[31m"$i"\033[34m" "║"
        }
        printf "\033[31m"$NF"\033[34m"
        print ""

        #line below header
        printf "\033[34m╠"
        for (i=0;i<length-1;i++) {
            if (i in arr) printf "╬"
            else printf "═"
        }
        printf"╣"
        print ""
    }
    NR!=1 {
        #prints a line
        printf "║ "
        for (i=1;i<NF;i++) {
            printf "\033[36m"$i"\033[34m" "║"
        }
        printf "\033[36m"$NF"\033[34m"
        print ""
    }
    END {
        #prints last line below the table
        printf "\033[34m╚"
        for (i=0;i<length-1;i++) {
            if (i in arr) printf "╩"
            else printf "═"
        }
        printf"╝"
        print ""
    }
    '
done