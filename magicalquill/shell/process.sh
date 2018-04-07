#!/bin/sh

process () {
    if [ "$SKIPPDF" != "1" ]; then
        if [ ! -d output-$2 ]; then
            rm -rf output
            decoupe-psup "$1"
            mv output output-$2
        fi
    fi
    rm -f ./$2
    cd output-$2
    for i in *.pdf; do
        j=$(basename $i .pdf)
        if [ ! -f $j.txt ]; then
            pdftotext $i
        fi
        sed -ne '/^.Projet de formation motiv.*Saisie/,/^_____/ p' < $j.txt | tail -n +8 | fmt -w 1 > $j.lm.txt
        echo $j"" >> ../$2
    done
    cd ..
}

if [ ! -f "CONFIG" ]; then
    echo "Il faut un fichier CONFIG au format:"
    echo "TAG:fichier.pdf"
fi

TAGS=""
while read line; do
    FILE="${line##*:}"
    TAG="${line%:*}"
    TAGS="$TAGS $TAG"
    if [ -n "$1" ]; then
        if [ "$TAG" = "$1" ]; then
            process $FILE $TAG
        fi
    else
        process $FILE $TAG
    fi
done < CONFIG
exit 0
