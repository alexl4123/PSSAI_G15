search_dir=instances
for entry in "$search_dir"/*
do
    echo "<<<<<<<<<<NOW-DOING-${entry##*/}>>>>>>>>>>>>>>"
    if test -f "tours/${entry##*/}_naive_tour"; then
        echo "---${entry##*/} Already exists - skipping ----"
    else
        now=$(date +"%T")
        echo "---The current starting time is: $now"
        (echo "---The current starting time is: $now") >> log.txt
        (time (python naive.py "$entry" >> log.txt)) >> log.txt
    fi
done
