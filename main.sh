#!/bin/bash
readpass(){
    local output=""
    while read -rsn1 char; do
        if [[ -z "$char" ]]; then
            break
        elif [[ $char == $'\177' || $char == $'\b' ]]; then
            if [ ${#output} -gt 0 ]; then
                output="${output%?}"
                printf "\b \b" >&2
            fi
        else
            output+="$char"
            printf '•' >&2
        fi
    done
    echo "$output"
}
printtitle() {
    clear
    printf "\033[32m"
    cat << 'EOF'

   ▄▄▄▄███▄▄▄▄    ▄█  ███▄▄▄▄    ▄█          ▄██████▄     ▄████████   ▄▄▄▄███▄▄▄▄      ▄████████         ▄█    █▄    ███    █▄  ▀█████████▄  
 ▄██▀▀▀███▀▀▀██▄ ███  ███▀▀▀██▄ ███         ███    ███   ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███        ███    ███   ███    ███   ███    ███ 
 ███   ███   ███ ███▌ ███   ███ ███▌        ███    █▀    ███    ███ ███   ███   ███   ███    █▀         ███    ███   ███    ███   ███    ███ 
 ███   ███   ███ ███▌ ███   ███ ███▌       ▄███          ███    ███ ███   ███   ███  ▄███▄▄▄           ▄███▄▄▄▄███▄▄ ███    ███  ▄███▄▄▄██▀  
 ███   ███   ███ ███▌ ███   ███ ███▌      ▀▀███ ████▄  ▀███████████ ███   ███   ███ ▀▀███▀▀▀          ▀▀███▀▀▀▀███▀  ███    ███ ▀▀███▀▀▀██▄  
 ███   ███   ███ ███  ███   ███ ███         ███    ███   ███    ███ ███   ███   ███   ███    █▄         ███    ███   ███    ███   ███    ██▄ 
 ███   ███   ███ ███  ███   ███ ███         ███    ███   ███    ███ ███   ███   ███   ███    ███        ███    ███   ███    ███   ███    ███ 
  ▀█   ███   █▀  █▀    ▀█   █▀  █▀          ████████▀    ███    █▀   ▀█   ███   █▀    ██████████        ███    █▀    ████████▀  ▄█████████▀  
                                                                                                                                             
                                                                                                
EOF
}
choose() {
    tput civis
    i=1
    for option in "$@"; do
        printf "\n\t\e[33m  $option\e[0m"
    done
    while true; do
        count=1
        printf "\033[$#A\r"
        for option in "$@"; do
            if((count==i)); then
                printf "\n\t\e[7m\e[33m> $option\e[0m"
            else
                printf "\n\t\e[33m  $option\e[0m"
            fi
            ((count++))
        done
        read -rsn1 key
        if [[ -z $key ]]; then
            tput cnorm
            return $i
        elif [[ $key == "A" ]]; then
            ((i--))
        elif [[ $key == "B" ]]; then
            ((i++))
        fi
        ((i<1)) && ((i++))
        ((i>$#)) && ((i--))
    done
}
signup() { #takes player number as argument
    printtitle
    if (($1==1)); then
        printf "\033[1m\033[34msignup for first player\n\033[0m"
    else 
        printf "\033[1m\033[34msignup for second player\n\033[0m"
    fi

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
        if ((${#username} < 4 )); then
            printf "\033[2K\r\033[31mUsername must be atleast 4 characters!"
        elif ((${#username} > 12 )); then
            printf "\033[2K\r\033[31mUsername must be atmost 12 characters!"
        elif [[ ! "$username" =~ ^[a-zA-Z][a-zA-Z0-9_]{3,11}$ ]]; then
            printf "\033[2K\r\033[31mUsername must not contain characters other than letters, digits, underscore!"
        elif grep -q "^$username	" users.tsv; then
            printf "\033[2K\r\033[31mUsername already exists!"
        else
            break
        fi
        printf "\033[1A\033[2K\r\033[36mPlease choose another username: "
    done
    printf "\033[2K\r\033[32mUsername successfully set as ${username}!\n"

    printf "\033[36m\nPlease choose a valid password.\n\033[90m"
    cat << 'EOF'
A valid password must contain 8-20 characters,
Password must contain at least 1 lowercase letter, 1 uppercase letter, 1 digit, and 1 special character(_@#$%^&*).
Password must not contain any other character than the one mentioned above, for example spaces.
You can't change your password later so choose wisely!
EOF
    printf "\033[36mEnter password: "
    local password
    local pattern='^[a-zA-Z0-9_@#$%^&*]{8,20}$'
    local patt='[_@#$%^&*]'
    while true; do
        printf "\033[35m"
        password=$(readpass)
        printf "\n"
        if ((${#password} < 8 )); then
            printf "\033[2K\r\033[31mPassword must contain at least 8 characters!"
        elif ((${#password} >20 )); then
            printf "\033[2K\r\033[31mPassword must contain at most 20 characters!"
        elif [[ ! "$password" =~ $pattern ]]; then
            printf "\033[2K\r\033[31mPassword must not contain characters not mentioned above!"
        elif [[ ! "$password" =~ [a-z] ]]; then
            printf "\033[2K\r\033[31mPassword must contain at least 1 lowercase letter!"
        elif [[ ! "$password" =~ [A-Z] ]]; then
            printf "\033[2K\r\033[31mPassword must contain at least 1 uppercase letter!"
        elif [[ ! "$password" =~ [0-9] ]]; then
            printf "\033[2K\r\033[31mPassword must contain at least 1 digit!"
        elif [[ ! "$password" =~ $patt ]]; then
            printf "\033[2K\r\033[31mPassword must contain at least 1 special character(_@#$%%^&*)!"
        else
            printf "\e[36mConfirm password: \033[35m"
            local confirmpassword=$(readpass)
            printf "\n"
            if [[ "$password" != "$confirmpassword" ]]; then
                printf "\033[2K\r\033[31mPasswords do not match!"
            else
                break
            fi
        fi
        printf "\033[1A\033[2K\r\033[36mPlease choose another password: "
    done
    printf "\033[2K\r\033[32mPassword successfully set!\n"

    local expected=$(echo -n "$password" | sha256sum | awk '{print $1}')
    echo -e "$username\t$expected" >> users.tsv

    if (($1==1)); then
        username1=$username
    else
        username2=$username
    fi
    printf "\033[32mPlayer logged in successfully!\n"
    choose "proceed"
}
checkpassword() { #takes username and player number as argument
    local username="$1"
    local expected=$(grep "^$username	" users.tsv | awk '{print $2}')
    local password
    while true; do
        printf "\033[36mEnter password: \033[35m"
        password=$(readpass)
        printf "\n"
        local pass=$(echo -n "$password" | sha256sum | awk '{print $1}')
        if [[ "${expected}" == "${pass}" ]]; then
            printf "\033[32mPlayer logged in successfully!\n"
            choose "proceed"
            if (($2==1)); then
                username1=$1
            else
                username2=$1
            fi
            break;
        else
            printf "\033[31mWrong password entered!\n"
            choose "try again" "go back to login/signup"
            var=$?
            if ((var==2)); then
                loginsignup $2
                break
            fi
        fi
        printf "\033[2K\r"
        printf "\033[1A\033[2K\r"
        printf "\033[1A\033[2K\r"
        printf "\033[1A\033\r"
        printf "\033[1A\033[2K\r"
    done
}
login() { #takes player number as argument
    while true; do
        printtitle
        if (($1==1)); then
            printf "\033[1m\033[34mlogin for first player\n\033[0m"
        else 
            printf "\033[1m\033[34mlogin for second player\n\033[0m"
        fi
        local username
        printf "\033[36m\nEnter username: \033[35m"
        read username
        if (($1==2)) && [[ "$username" == "$username1" ]]; then
            printf "\033[33mYou can't play with yourself!\nSecond player should have different username.\n"
        elif grep -q "^$username	" users.tsv; then
            checkpassword "${username}" "$1"
            break
        else
            printf "\033[31mUser ${username} doesn't exist!\n"
        fi
        choose "signup as a new user" "try another username"
        var=$?
        if ((var==1)); then
            signup $1
            break
        fi
    done
}
loginsignup(){ #takes player number as argument
    printtitle
    if (($1==1)); then
        printf "\n\033[1m\033[34mHello first player!\n\033[0m"
    else 
        printf "\n\033[1m\033[34mHello second player!\n\033[0m"
    fi
    choose "signup as a new user" "login as an existing user"
    var=$?
    if ((var==1)); then
        signup $1
    else
        login $1
    fi
}

printtitle
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
choose "START GAMEHUB"

while true; do
    printtitle
    choose "play" "leaderboard"
    var=$?
    if ((var==2)); then
        printtitle
        printf "By which metric do you want it to be sorted:\n"
        choose "Username" "Wins" "Draws" "Losses" "Wins/Losses"
        bash leaderboard.sh $?
    else
        break
    fi
done

loginsignup 1

loginsignup 2

printtitle
printf "\n\033[0mPlayer 1: ${username1}\nPlayer 2:3
 ${username2}\n"
cat << 'EOF'
      ___ ___    ___       ___     __              ___     __   ___  __         
|    |__   |      |  |__| |__     / _`  /\   |\/| |__     |__) |__  / _` | |\ | 
|___ |___  |      |  |  | |___    \__> /~~\  |  | |___    |__) |___ \__> | | \| 

EOF

python3 game.py "${username1}" "${username2}"
