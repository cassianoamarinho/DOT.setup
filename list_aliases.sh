#!/bin/bash
count=0
function process_line() {
    line=$1
    line_splited=(${line//=/ })
    alias_cmd=${line_splited[1]}

    if [[ ${alias_cmd} != "" ]]; then
        text="$alias_cmd"
        text="${text} - $(echo "$1" | awk -F' # ' '{print $2}')"
        echo "${text}"
    fi
}

echo "#########################"
echo "### list aliases #######"
echo "#########################"
echo ""

while IFS='' read -r LinefromFile || [[ -n "${LinefromFile}" ]]; do
    ((count++))
    process_line "$LinefromFile"
done < "$HOME/.bash_aliases"
