
if [ ! -d "build" ]; then
  mkdir build
fi

pdflatex -jobname=report -output-directory=build Main
