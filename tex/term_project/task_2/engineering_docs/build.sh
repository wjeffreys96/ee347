if [ ! -d "build" ]; then
  mkdir build
fi

pdflatex -jobname=report -output-directory=build Main
makeglossaries -d build report
bibtex build/report
pdflatex -jobname=report -output-directory=build Main
pdflatex -jobname=report -output-directory=build Main
