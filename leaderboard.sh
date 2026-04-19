#!/bin/bash
clear
printf "\033[32m"
cat << 'EOF'

██╗     ███████╗ █████╗ ██████╗ ███████╗██████╗ ██████╗  ██████╗  █████╗ ██████╗ ██████╗ 
██║     ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
██║     █████╗  ███████║██║  ██║█████╗  ██████╔╝██████╔╝██║   ██║███████║██████╔╝██║  ██║
██║     ██╔══╝  ██╔══██║██║  ██║██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
███████╗███████╗██║  ██║██████╔╝███████╗██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 

EOF
games="Tic-Tac-Toe Othello Connect4 Chain-Reaction"
metric=$1
[[ $metric == "Username" ]] && sort_option="-k1,1"
[[ $metric == "Wins" ]] && sort_option="-n -k2,2r -k4,4 -k3,3"
[[ $metric == "Win percent" ]] && sort_option="-k5,5r -k7,7"
[[ $metric == "Losses" ]] && sort_option="-n -k4,4r -k2,2 -k3,3r"
[[ $metric == "Loss percent" ]] && sort_option="-k7,7r -k5,5"
[[ $metric == "Wins/Losses" ]] && sort_option="-g -k8,8r -k2,2 -k3,3"
for game in $games; do
    printf "\033[1;35m\n${game^^}\n\n\033[0m"
    awk -v game="$game" '
    BEGIN {
        FS=","
        OFS=","
    }
    $4==game && $5=="False" {
        data[$1]["win"]++
        data[$2]["loss"]++
    }
    $4==game && $5=="True" {
        data[$1]["draw"]++
        data[$2]["draw"]++
    }
    END {
        for(i in data){
            win_p=100*(data[i]["win"]+0)/(data[i]["win"]+data[i]["draw"]+data[i]["loss"])
            draw_p=100*(data[i]["draw"]+0)/(data[i]["win"]+data[i]["draw"]+data[i]["loss"])
            loss_p=100*(data[i]["loss"]+0)/(data[i]["win"]+data[i]["draw"]+data[i]["loss"])
            wbyl=(data[i]["loss"]+0 == 0) ? "inf" : (data[i]["win"]+0)/(data[i]["loss"]+0)
            printf "%s,%d,%d,%d,%8.4f,%8.4f,%8.4f,%s,\n", i,data[i]["win"]+0,data[i]["draw"]+0,data[i]["loss"]+0,win_p,draw_p,loss_p,wbyl
        }
    }
    ' history.csv | sort -t ',' $sort_option | (echo "Username,Wins,Draws,Losses,Win%,Draw%,Loss%,Wins/Losses,"; cat -;) | column -t -s "," -o "    ▐ " | awk -F"▐" '
    NR==1 {
        temp=0
        for(i=1;i<=NF;i++){
            temp+=length($i)+1
            arr[temp]
        }
        for(i in arr){
        
        }
        printf "\033[34m▛"
        for (i=0;i<length;i++) {
            if (i in arr) printf "▜"
            else printf "▀"
        }
        print ""
        printf "▌ "
        for (i=1;i<NF;i++) {
            printf "\033[31m"$i"\033[34m" "▐"
        }
        printf "\033[31m"$NF"\033[34m"
        print ""
        printf "\033[34m▙"
        for (i=0;i<length;i++) {
            if (i in arr) printf "▟"
            else printf "▄"
        }
        print ""
    }
    NR!=1 {
        printf "▌ "
        for (i=1;i<NF;i++) {
            printf "\033[36m"$i"\033[34m" "▐"
        }
        printf "\033[36m"$NF"\033[34m"
        print ""
    }
    END {
        printf "\033[34m▙"
        for (i=0;i<length;i++) {
            if (i in arr) printf "▟"
            else printf "▄"
        }
        print ""
    }
    '
done