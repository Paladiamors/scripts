export PATH=$PATH:~/scripts/bin
#github related commands
alias github-login='curl -u "paladiamors" https://api.github.com'
alias github-get-repositories='curl https://api.github.com/users/paladiamors/repos -s | grep \"name\" | cut -d \" -f 4'
alias ga='git add *'
alias gc='git commit -m'
alias gp='git push' 


#add the code in .bashrc if you want 
#it to automatically load the script on loadup
function reload-preferences { 
for f in ~/scripts/*.sh; do
   . $f
done
}

function code {
    # https://stackoverflow.com/questions/394230/how-to-detect-the-os-from-a-bash-script
    # see this to add os types
    if [[ $OSTYPE == "darwin"* ]]; then
        /Applications/Visual\ Studio\ Code.app/Contents/MacOS/Electron $1
    else
        # add something for the ubuntu case
        echo "test"
    fi
}

function docker-bash {
    docker exec -it $1 sh
}
