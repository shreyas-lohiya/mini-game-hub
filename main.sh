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
printf "\033[36m\nTo get started, grab a friend and have both players log in.\n\n"
signup() { #takes player number as argument
    printf "\033[36m\nPlease choose a valid username.\n\033[90m"
    cat << 'EOF'
A valid username must contain 4-12 characters,
allowed characters include upper and lowercase letters(A-Z, a-z), digits(0-9), underscore(_).
It must start with a letter(A-Z or a-z).
You can't change your username later so choose wisely!
EOF
    printf "\033[36mEnter username: "
    local username
    while true; do
        printf "\033[35m"
        read username
        if [[ ! "$username" =~ ^[a-zA-Z][a-zA-Z0-9_]{3,11}$ ]]; then
            printf "\033[31mInvalid username!\n\033[36mPlease choose another username: "
            continue
        fi
        if grep -q "^$username " users.tsv; then
            printf "\033[31mUsername already exists!\n\033[36mPlease choose another username: "
            continue
        fi
        break;
    done
    printf "\033[32mUsername successfully set as ${username}!\n\n\033[36mPlease choose a valid password.\n\033[90m"
    cat << 'EOF'
A valid password must contain 8-20 characters,
Password must contain at least 1 lowercase letter, 1 uppercase letter, 1 digit, and 1 special character(_@#$%^&*).
Password must not contain any other character than the one mentioned above, for example spaces.
You can't change your password later so choose wisely!
EOF
    printf "\033[36mEnter password: "
    local password
    while true; do
        read -s password
        echo
        local pattern='^[a-zA-Z0-9_@#$%^&*]{8,20}$'
        if [[ ! "$password" =~ $pattern ]]; then
            printf "\033[31mInvalid password!\n\033[36mPlease choose another password: "
            continue
        fi
        if [[ ! "$password" =~ [a-z] ]]; then
            printf "\033[31mPassword must contain at least 1 lowercase letter!\n\033[36mPlease choose another password: "
            continue
        fi
        if [[ ! "$password" =~ [A-Z] ]]; then
            printf "\033[31mPassword must contain at least 1 uppercase letter!\n\033[36mPlease choose another password: "
            continue
        fi
        if [[ ! "$password" =~ [0-9] ]]; then
            printf "\033[31mPassword must contain at least 1 digit!\n\033[36mPlease choose another password: "
            continue
        fi
        local patt='[_@#$%^&*]'
        if [[ ! "$password" =~ $patt ]]; then
            printf "\033[31mPassword must contain at least 1 special character(_@#$%^&*)!\n\033[36mPlease choose another password: "
            continue
        fi
        local confirmpassword
        read -sp "Confirm password: " confirmpassword
        echo
        if [[ "$password" != "$confirmpassword" ]]; then
            printf "\033[31mPasswords do not match!\n\033[36mPlease choose another password: "
            continue
        fi
        break;
    done
    printf "\033[32mPassword successfully set!\n"
    local expected=$(echo -n "$password" | sha256sum | awk '{print $1}')
    echo -e "$username\t$expected" >> users.tsv
    if [[ "$1" == "1" ]]; then
        username1=$username
    else
        username2=$username
    fi
    printf "\033[32mPlayer logged in successfully!\n"
}
userdne() { #takes player number as argument
    while true; do
        printf "\033[35m"
        read sign
        if [[ "${sign}" == "y" || "${sign}" == "Y" ]]; then
            signup $1
            break
        elif [[ "${sign}" == "n" || "${sign}" == "N" ]]; then
            enteruser $1
            break
        else 
            printf "\033[36mPlease enter y if you want to signup or n if you want to login through a different user: "
        fi
    done
}
checkpassword() { #takes expected hash, player number and username as argument
    local expected=$1
    while true; do
        printf "\033[36mEnter password: "
        read -s pass
        echo
        local password=$(echo -n "$pass" | sha256sum | awk '{print $1}')
        if [[ "${expected}" == "${password}" ]]; then
            printf "\033[32mPlayer logged in successfully!\n"
            if [[ "$2" == "1" ]]; then
                username1=$3
            else
                username2=$3
            fi
            break;
        else
            printf "\033[31mWrong password entered!\n\033[36mDo you want to try again ? [y/n]: "
            while true; do
                printf "\033[35m"
                read again
                if [[ "${again}" == "y" || "${again}" == "Y" ]]; then
                    break;
                elif [[ "${again}" == "n" || "${again}" == "N" ]]; then
                    loginsignup $2
                    return;
                else 
                printf "\033[36mPlease enter y if you want to try again or n if you want to login/signup through a different user: "
                fi
            done
        fi
    done
}
enteruser() { #takes player number as argument
    local username
    while true; do
        printf "\033[36mEnter username: \033[35m"
        read username
        if [[ "$1" == "1" ]]; then
            break
        else
            if [[ "$username" == "$username1" ]]; then
                printf "\033[33mYou can't play with yourself!\nSecond player should have different username.\n"
            else
                break
                fi
        fi
    done
    if grep -q "^$username	" users.tsv; then
        local expected=$(grep "^$username	" users.tsv | awk '{print $2}')
        checkpassword "$expected" "$1" "${username}"
    else
        printf "\033[31mUser ${username} doesn't exist!\n\033[36mDo you want to sign up? [y/n]: "
        userdne $1
    fi
}
loginsignup(){ #takes player number as argument
    printf "\033[36mDo you want to sign up as a new user/Are you playing for the first time? [y/n]: "
    while true; do
        printf "\033[35m"
        read first
        if [[ "${first}" == "y" || "${first}" == "Y" ]]; then
            signup $1
            break;
        elif [[ "${first}" == "n" || "${first}" == "N" ]]; then
            enteruser $1
            break;
        else 
            printf "\033[36mPlease enter y if you want to sign up or n if you want to login to a pre-existing user: "
        fi
    done
}
printf "\033[36mHello first player!\n"
loginsignup "1"
printf "\n\033[36mHello second player!\n"
loginsignup "2"
printf "\n\033[0mPlayer 1: ${username1}\nPlayer 2: ${username2}\n"
cat << 'EOF'
      ___ ___    ___       ___     __              ___     __   ___  __         
|    |__   |      |  |__| |__     / _`  /\   |\/| |__     |__) |__  / _` | |\ | 
|___ |___  |      |  |  | |___    \__> /~~\  |  | |___    |__) |___ \__> | | \| 

EOF

python3 game.py "${username1}" "${username2}"
