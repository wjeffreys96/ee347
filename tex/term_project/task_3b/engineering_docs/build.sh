if [ ! -d "build" ]; then
  mkdir build
fi

pdflatex -interaction=nonstopmode -jobname=report -output-directory=build Main
makeglossaries -d build report
bibtex build/report
pdflatex -interaction=nonstopmode -jobname=report -output-directory=build Main
pdflatex -interaction=nonstopmode -jobname=report -output-directory=build Main
