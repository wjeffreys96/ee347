
if [ ! -d "build" ]; then
  mkdir build
fi

pdflatex -interaction=nonstopmode -jobname=report -output-directory=build Main
