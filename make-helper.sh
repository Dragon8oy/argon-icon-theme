#!/bin/bash
generateImage() {
  filename="$1"
  read -ra iconResolutions <<< "$2"
  for resolution in "${iconResolutions[@]}"; do
    inputFile="argon/icons${filename/build\/resolution\/apps}"
    inputFile="${inputFile//.png/.svg}"
    outputFile="${filename//resolution/$resolution\x$resolution}"
    echo "$inputFile -> $outputFile"
    mkdir -p "./build/${resolution}x${resolution}/apps"
    inkscape "--export-filename=$outputFile" -w "$resolution" -h "$resolution" "$inputFile" > /dev/null 2>&1
    optipng -strip all "$outputFile"
  done
  cp "$inputFile" "./build/scalable/apps/"
}

createIndex() {
  read -ra iconResolutions <<< "$2"
  cp "./argon/index.theme" "$1"
  for resolution in "${iconResolutions[@]}" scalable; do
    if [[ "$resolution" != "scalable" ]]; then
      resolution="${resolution}x${resolution}"
    fi
    sed "s|^Directories=.*|&$resolution/apps,|" ./build/index.theme > ./build/index.theme.temp
    resolution="${resolution%%x*}"
    echo "" >> ./build/index.theme.temp
    fileContent="$(cat ./argon/directory.template)"
    fileContent="${fileContent//Size=/Size=$resolution}"
    if [[ "$resolution" != "scalable" ]]; then
      fileContent="${fileContent//resolution/$resolution\x$resolution}"
      fileContent="${fileContent//Type=/Type=Threshold}"
    else
      fileContent="${fileContent//resolution/$resolution}"
      fileContent="${fileContent//Type=/Type=Scalable}"
    fi
    echo "$fileContent" >> ./build/index.theme.temp
    mv ./build/index.theme.temp ./build/index.theme
  done
  sed 's/,$//' ./build/index.theme > ./build/index.theme.temp
  mv ./build/index.theme.temp ./build/index.theme
}

case $1 in
  -i|--images) generateImage "$2" "$3"; exit;;
  -t|--theme-index) createIndex "$2" "$3"; exit;;
esac
