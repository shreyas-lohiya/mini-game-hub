#!/bin/bash
clear
games="tictactoe othello connect4"
metric=$1
sort_option="-n -k8,8r -k4,4r"
[[ "$metric" -eq 1 ]] && sort_option="-n -k4,4r -k6,6"
[[ "$metric" -eq 2 ]] && sort_option="-n -k6,6r -k4,4"
for game in $games; do
    echo
    echo ${game^^}
    echo
    awk -v game="$game" '
    BEGIN {
        FS=","
    }
    $4==game {
        data[$1]["win"]++
        data[$2]["loss"]++
    }
    END {
        for(i in data){
            print "▌",i,"▌",data[i]["win"]+0,"▌",data[i]["loss"]+0,"▌",(data[i]["loss"]+0 == 0) ? "inf" : (data[i]["win"]+0)/(data[i]["loss"]+0), (data[i]["win"]+0)/(data[i]["loss"]+0+data[i]["win"]),"▐"
        }
    }
    ' history.csv | sort $sort_option | cut -d " " -f 1,2,3,4,5,6,7,8,10 | (echo "▌ User ▌ Wins ▌ Losses ▌ Wins/Losses ▐"; cat -;) | column -t -o "   " | awk -F'▌' '
    START {
        
    }
    NR==1 {
        for (i=0;i<length;i++) {
            if (i==length($1) || i==length($1)+length($2)+1 || i==length($1)+length($2)+length($3)+2 || i==length($1)+length($2)+length($3)+length($4)+3 || i==length($1)+length($2)+length($3)+length($4)+length($5)+4) printf "▛"
            else if(i<length-1) printf "▀"
            else printf "▜"
        }
        print ""
        print
        for (i=0;i<length;i++) {
            if (i==length($1) || i==length($1)+length($2)+1 || i==length($1)+length($2)+length($3)+2 || i==length($1)+length($2)+length($3)+length($4)+3 || i==length($1)+length($2)+length($3)+length($4)+length($5)+4) printf "▙"
            else if(i<length-1) printf "▄"
            else printf "▟"
        }
        print ""
    }
    NR!=1 {
        print
    }
    END {
        for (i=0;i<length;i++) {
            if (i==length($1) || i==length($1)+length($2)+1 || i==length($1)+length($2)+length($3)+2 || i==length($1)+length($2)+length($3)+length($4)+3 || i==length($1)+length($2)+length($3)+length($4)+length($5)+4) printf "▙"
            else if(i<length-1) printf "▄"
            else printf "▟"
        }
        print ""
    }
    '
done
