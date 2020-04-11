zenity --info --text="Beginning Backup"
rsync -avl --delete --stats --progress --exclude "Drives/*" ~/ ~/Drives/2.1TB-backup/Backups/Home\ backup
rsync -avl --delete --stats --progress ~/Drives/1.1TB/Pictures/ ~/Drives/2.1TB-backup/Backups/Pictures\ backup
rsync -avl --delete --stats --progress ~/Drives/1.1TB/Music/ ~/Drives/2.1TB-backup/Backups/Music\ backup


