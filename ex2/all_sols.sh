search_dir=../instances

echo "" > log.txt
echo "" > log2.txt

for entry in "$search_dir"/*
do
    echo "<<<<<<<<<<NOW-DOING-${entry##*/}>>>>>>>>>>>>>>"
    now=$(date +"%T")
    echo "---The current starting time is: $now"
    (echo "---The current starting time is: $now") >> log.txt

    (time (python start_all.py -f "../ex1/tours/${entry##*/}_tour" "$entry" >> log2.txt)) 2>> log.txt
    #(time (python start_all.py "$entry" >> log2.txt)) 2>> log.txt
done
