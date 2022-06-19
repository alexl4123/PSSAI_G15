search_dir=solutions_from_known_best/tours

echo "" > log.txt
echo "" > log2.txt

for entry in "$search_dir"/*
do
    echo "<<<<<<<<<<NOW-DOING-${entry##*/}>>>>>>>>>>>>>>"
    now=$(date +"%T")
    echo "---The current starting time is: $now"
    (echo "---The current starting time is: $now") >> log.txt

    arrFirst=(${entry##*/})
    arrIN=(${arrFirst//_/ })

    (time (python src/check_wpp.py "../instances/${arrIN[0]}" "$entry" >> log2.txt)) 2>> log.txt
done
