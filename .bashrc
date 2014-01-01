export PATH=$PATH:~/scripts
alias ls='ls -lrtG'

#github related commands
alias github-login='curl -u "paladiamors" https://api.github.com'
alias github-get-repositories='curl https://api.github.com/users/paladiamors/repos -s | grep \"name\" | cut -d \" -f 4'
alias ga='git add *'
alias gc='git commit -m'
alias gp='git push' 
