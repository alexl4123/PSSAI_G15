search_dir=instances
for entry in "$search_dir"/*
do
    echo "<<<<<<<<<<NOW-DOING-${entry##*/}>>>>>>>>>>>>>>"
    if test -f "tours/${entry##*/}_tour"; then
        echo "---${entry##*/} Already exists - skipping ----"
    else
        now=$(date +"%T")
        echo "---The current starting time is: $now"
        (echo "---The current starting time is: $now") >> log.txt
        (time (python wins_algorithm.py "$entry" >> log.txt)) >> log.txt
    fi
done
