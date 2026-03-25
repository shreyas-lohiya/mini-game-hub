#!/bin/bash
clear
printf "\033[32m"
cat << 'EOF'

███╗   ███╗██╗███╗   ██╗██╗     ██████╗  █████╗ ███╗   ███╗███████╗    ██╗  ██╗██╗   ██╗██████╗ 
████╗ ████║██║████╗  ██║██║    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██║  ██║██║   ██║██╔══██╗
██╔████╔██║██║██╔██╗ ██║██║    ██║  ███╗███████║██╔████╔██║█████╗      ███████║██║   ██║██████╔╝
██║╚██╔╝██║██║██║╚██╗██║██║    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██╔══██║██║   ██║██╔══██╗
██║ ╚═╝ ██║██║██║ ╚████║██║    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ██║  ██║╚██████╔╝██████╔╝
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ 
                                                                                                
EOF
printf "\033[35m"
cat << 'EOF'
_______________________________________________________________________________________________
|Welcome, players, to the Mini Game Hub!                                                       |
|Step into a collection of exciting two-player,                                                |
|turn-based games where only strategy and skill decide the winner.                             |
|Challenge your opponent, outplay every move, and show the world what you’re truly capable of. |
|Play smart! Compete hard! Most importantly have fun!                                          |
|May the best player win!                                                                      |
|______________________________________________________________________________________________|
EOF
echo
printf "\033[36m"
echo "To get started, grab a friend and have both players log in."
echo
signup() { #takes player number as argument
    echo
    printf "\033[36m"
    echo "Please choose a valid username."
    printf "\033[30m"
    echo "A valid username must contain 4-12 characters,"
    echo "allowed characters include upper and lowercase letters(A-Z, a-z), digits(0-9), underscore(_)."
    echo "It must start with a letter(A-Z or a-z)."
    echo "You can't change your username later so choose wisely!"
    printf "\033[36m"
    printf "Enter username: "
    local username
    while true; do
        read username
        if [[ ! "$username" =~ ^[a-zA-Z][a-zA-Z0-9_]{3,11}$ ]]; then
            printf "\033[31m"
            echo "Invalid username!"
            printf "\033[36m"
            printf "Please choose another username: "
            continue
        fi
        if grep -q "^$username " users.tsv; then
            printf "\033[31m"
            echo "Username already exists!"
            printf "\033[36m"
            printf "Please choose another username: "
            continue
        fi
        break;
    done
    printf "\033[32m"
    echo "Username successfully set as ${username}!"
    echo
    printf "\033[36m"
    echo "Please choose a valid password."
    printf "\033[30m"
    echo "A valid password must contain 8-20 characters,"
    echo "Password must contain at least 1 lowercase letter, 1 uppercase letter, 1 digit, and 1 special character(_@#$%^&*)."
    echo "Password must not contain any other character than the one mentioned above, for example spaces."
    echo "You can't change your password later so choose wisely!"
    printf "\033[36m"
    printf "Enter password: "
    local password
    while true; do
        read -s password
        echo
        local pattern='^[a-zA-Z0-9_@#$%^&*]{8,20}$'
        if [[ ! "$password" =~ $pattern ]]; then
            printf "\033[31m"
            echo "Invalid password!"
            printf "\033[36m"
            printf "Please choose another password: "
            continue
        fi
        if [[ ! "$password" =~ [a-z] ]]; then
            printf "\033[31m"
            echo "Password must contain at least 1 lowercase letter!"
            printf "\033[36m"
            printf "Please choose another password: "
            continue
        fi
        if [[ ! "$password" =~ [A-Z] ]]; then
            printf "\033[31m"
            echo "Password must contain at least 1 uppercase letter!"
            printf "\033[36m"
            printf "Please choose another password: "
            continue
        fi
        if [[ ! "$password" =~ [0-9] ]]; then
            printf "\033[31m"
            echo "Password must contain at least 1 digit!"
            printf "\033[36m"
            printf "Please choose another password: "
            continue
        fi
        local patt='[_@#$%^&*]'
        if [[ ! "$password" =~ $patt ]]; then
            printf "\033[31m"
            echo "Password must contain at least 1 special character(_@#$%^&*)!"
            printf "\033[36m"
            printf "Please choose another password: "
            continue
        fi
        local confirmpassword
        read -sp "Confirm password: " confirmpassword
        echo
        if [[ "$password" != "$confirmpassword" ]]; then
            printf "\033[31m"
            echo "Passwords do not match!"
            printf "\033[36m"
            printf "Please choose another password: "
            continue
        fi
        break;
    done
    printf "\033[32m"
    echo "Password successfully set!"
    local expected=$(echo -n "$password" | sha256sum | awk '{print $1}')
    echo "$username $expected" >> users.tsv
    if [[ "$1" == "1" ]]; then
        username1=$username
    else
        username2=$username
    fi
}
userdne() { #takes player number as argument
    while true; do
        read sign
        if [[ "${sign}" == "y" || "${sign}" == "Y" ]]; then
            signup $1
            break
        elif [[ "${sign}" == "n" || "${sign}" == "N" ]]; then
            enteruser $1
            break
        else 
            printf "\033[36m"
            printf "Please enter y if you want to signup or n if you want to login through a different user: "
        fi
    done
}
checkpassword() { #takes expected hash, player number and username as argument
    local expected=$1
    while true; do
        read -sp "Enter password: " pass
        echo
        local password=$(echo -n "$pass" | sha256sum | awk '{print $1}')
        if [[ "${expected}" == "${password}" ]]; then
            printf "\033[32m"
            echo "Player logged in successfully!"
            if [[ "$2" == "1" ]]; then
                username1=$3
            else
                username2=$3
            fi
            break;
        else
            printf "\033[31m"
            echo "Wrong password entered!"
            printf "\033[36m"
            printf "Do you want to try again ? [y/n]: "
            while true; do
                read again
                if [[ "${again}" == "y" || "${again}" == "Y" ]]; then
                    break;
                elif [[ "${again}" == "n" || "${again}" == "N" ]]; then
                    enteruser $2
                    return;
                else 
                printf "\033[36m"
                printf "Please enter y if you want to try again or n if you want to login through a different user: "
                fi
            done
        fi
    done
}
enteruser() { #takes player number as argument
    local username
    while true; do
        read -p "Enter username: " username
        if [[ "$1" == "1" ]]; then
            break
        else
            if [[ "$username" == "$username1" ]]; then
                printf "\033[33m"
                echo "You can't play with yourself!"
                echo "Second player should have different username."
                printf "\033[36m"
            else
                break
                fi
        fi
    done
    if grep -q "^$username " users.tsv; then
        local expected=$(grep "^$username " users.tsv | awk '{print $2}')
        checkpassword "$expected" "$1" "${username}"
    else
        printf "\033[31m"
        echo "User ${username} doesn't exist!"
        printf "\033[36m"
        printf "Do you want to sign up? [y/n]: "
        userdne $1
    fi
}
loginsignup(){ #takes player number as argument
    printf "\033[36m"
    printf "Do you want to sign up as a new user/Are you playing for the first time? [y/n]: "
    while true; do
        read first
        if [[ "${first}" == "y" || "${first}" == "Y" ]]; then
            signup $1
            break;
        elif [[ "${first}" == "n" || "${first}" == "N" ]]; then
            enteruser $1
            break;
        else 
            printf "\033[36m"
            printf "Please enter y if you want to sign up or n if you want to login to a pre-existing user: "
        fi
    done
}
printf "\033[36m"
echo "Hello first player!"
loginsignup "1"
echo 
printf "\033[36m"
echo "Hello second player!"
loginsignup "2"
echo
printf "\033[0m"
echo "Player 1: ${username1}"
echo "Player 2: ${username2}"
cat << 'EOF'
      ___ ___    ___       ___     __              ___     __   ___  __         
|    |__   |      |  |__| |__     / _`  /\   |\/| |__     |__) |__  / _` | |\ | 
|___ |___  |      |  |  | |___    \__> /~~\  |  | |___    |__) |___ \__> | | \| 

EOF

python3 game.py "${username1}" "${username2}"
